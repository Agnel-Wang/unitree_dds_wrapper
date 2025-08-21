from unitree_dds_wrapper.idl.unitree_api.msg import dds_
from unitree_dds_wrapper.publisher import Publisher, RequestPublisher
from unitree_dds_wrapper.subscription import Subscription
import time
import threading
import copy
from typing import Tuple

UT_ROBOT_ERR_CLIENT_API_TIMEOUT = 3104
UT_ROBOT_ERR_SERVER_API_PARAMETER = 3204

class ResponseTimeoutError(TimeoutError):
    """Raised when waiting for a DDS response times out."""
    def __init__(self, request_id):
        super().__init__(f"Timeout waiting for response to request_id={request_id}")
        self.request_id = request_id

class ResponseSubscriber(Subscription):
    def __init__(self, topic):
        super().__init__(dds_.Response_, topic)
        self.msg: dds_.Response_
        self._dict_lock = threading.Lock()
        self._responses: dict[int, dds_.Response_] = {}      # request_id -> response
        self._events: dict[int, threading.Event] = {}         # request_id -> Event
        self._pending_request_ids: set[int] = set()           # 正在等待的 request_id

    # 发送前调用，预注册要等待的 request_id，避免响应先到被丢
    def expect(self, request_id: int):
        with self._dict_lock:
            if request_id not in self._events:
                self._events[request_id] = threading.Event()
            self._pending_request_ids.add(request_id)

    def post_communication(self):
        # 仅接收自己等待的请求的响应；其他一律丢弃
        req_id = self.msg.header.identity.id
        with self._dict_lock:
            if req_id in self._pending_request_ids:
                # 深拷贝一次，避免底层 msg 被后续覆盖
                self._responses[req_id] = copy.deepcopy(self.msg)
                ev = self._events.get(req_id)
                if ev:
                    ev.set()  # 通知等待线程
            # else: 非自己请求或已超时清理过的请求，直接丢弃

    def get(self, request_id: int, timeout = None) -> dds_.Response_:
        # 若未 expect，也给一次兜底；但建议总是先 expect 再发送
        with self._dict_lock:
            ev = self._events.get(request_id)
            if ev is None:
                ev = threading.Event()
                self._events[request_id] = ev
            self._pending_request_ids.add(request_id)

        if not ev.wait(timeout):
            # 超时：彻底清理该 request_id 的痕迹，迟到响应将被丢弃
            with self._dict_lock:
                self._events.pop(request_id, None)
                self._responses.pop(request_id, None)
                self._pending_request_ids.discard(request_id)
            raise ResponseTimeoutError(request_id)

        with self._dict_lock:
            resp = self._responses.pop(request_id, None)
            # 无论如何都清理（防止重复占用）
            self._events.pop(request_id, None)
            self._pending_request_ids.discard(request_id)

        if resp is None:
            raise ResponseTimeoutError(request_id)

        return resp


class Client:
    def __init__(self, name: str):
        self._pub = RequestPublisher(topic=f"rt/api/{name}/request", message=dds_.Request_)
        self._sub = ResponseSubscriber(topic=f"rt/api/{name}/response")
        self.timeout_s = 1.0

    def call(self, api_id: int, parameter: str) -> Tuple[int, str]:
        # 生成唯一请求 ID（也可以用 uuid/int 计数器）
        request_id = time.monotonic_ns()

        # 先注册等待的 request_id，防止响应先到被丢
        self._sub.expect(request_id)

        # 发送请求
        self._pub.msg.parameter = parameter
        self._pub.msg.header.identity.id = request_id
        self._pub.msg.header.identity.api_id = api_id
        self._pub.write()

        # 等待对应响应
        try:
            response = self._sub.get(request_id, timeout=self.timeout_s)
        except ResponseTimeoutError:
            return UT_ROBOT_ERR_CLIENT_API_TIMEOUT, "Request timed out"

        return response.header.status.code, response.data
