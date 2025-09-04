from unitree_dds_wrapper.idl.unitree_api.msg import dds_
from unitree_dds_wrapper.publisher import Publisher
from unitree_dds_wrapper.subscription import Subscription, RequestSubscription
from typing import Callable
from threading import Thread
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor
from enum import IntEnum

UT_ROBOT_ERR_CLIENT_API_NOT_REG = 3103
UT_ROBOT_ERR_SERVER_INTERNAL = 3202

class ResponsePublisher(Publisher):
    def __init__(self, topic):
        super().__init__(dds_.Response_, topic)
        self.msg: dds_.Response_

class Server:
    def __init__(self, name: str):
        # 只确保了请求一定会被处理; 响应直接发送
        self._pub = ResponsePublisher(topic=f"rt/api/{name}/response") 
        self._sub = RequestSubscription(topic=f"rt/api/{name}/request", message=dds_.Request_,
            handler=self.sub_handler
        )
        self._handlers = {}
        self._loop = asyncio.new_event_loop()
        self._executor = ThreadPoolExecutor(max_workers=4)

    def start(self):
        # 启动 asyncio 事件循环线程
        self._thread = Thread(target=self._loop.run_forever, daemon=True)
        self._thread.start()

    # handler: [](str) -> (int, str)
    def register(self, api_id: int, handler: Callable):
        if api_id in self._handlers:
            raise ValueError(f"Handler for ID {api_id} already registered.")
        self._handlers[api_id] = handler

    def sub_handler(self, _):
        request = self._sub.take_one()
        if request is None:
            return
        api_id = request.header.identity.api_id
        if api_id in self._handlers:
            handler = self._handlers[api_id]
            future = asyncio.run_coroutine_threadsafe(
                self._handle_request(request, handler),
                self._loop
            )
        else:
            msg = dds_.Response_()
            msg.data = ""
            msg.header.identity.id = request.header.identity.id
            msg.header.identity.api_id = api_id
            msg.header.status.code = UT_ROBOT_ERR_CLIENT_API_NOT_REG
            self._pub.write(msg)

    async def _handle_request(self, request: dds_.Request_, handler):
        api_id = request.header.identity.api_id
        try:
            if asyncio.iscoroutinefunction(handler):
                ret = await handler(request.parameter)
            else:
                ret = await self._loop.run_in_executor(
                    self._executor, handler, request.parameter
                )
            if isinstance(ret, IntEnum): # 支持状态码
                ret = (ret.value, ret.name)
        except Exception as e:
            ret = (-1, str(e))

        code, response = ret
        msg = dds_.Response_()
        msg.data = response
        msg.header.identity.id = request.header.identity.id
        msg.header.identity.api_id = api_id
        msg.header.status.code = code
        self._pub.write(msg)