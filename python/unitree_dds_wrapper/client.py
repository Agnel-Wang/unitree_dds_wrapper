from unitree_dds_wrapper.idl.unitree_api.msg import dds_
from unitree_dds_wrapper.publisher import Publisher
from unitree_dds_wrapper.subscription import Subscription
import queue
import time

UT_ROBOT_ERR_CLIENT_API_TIMEOUT = 3104
UT_ROBOT_ERR_SERVER_API_PARAMETER = 3204

class RequestPublisher(Publisher):
    def __init__(self, topic):
        super().__init__(dds_.Request_, topic)
        self.msg: dds_.Request_

class ResponseSubscriber(Subscription):
    def __init__(self, topic):
        super().__init__(dds_.Response_, topic)
        self.msg: dds_.Response_
        self._queue = queue.Queue(10)

    def post_communication(self):
        self._queue.put(self.msg)

    def get(self, timeout = None) -> dds_.Response_:
        return self._queue.get(block=True, timeout=timeout)
    
class Client:
    def __init__(self, name: str):
        self._pub = RequestPublisher(topic=f"rt/api/{name}/request")
        self._sub = ResponseSubscriber(topic=f"rt/api/{name}/response")
        self.timeout_s = 1.0

    def call(self, api_id: int, parameter: str) -> tuple[int, str]:
        self._pub.msg.parameter = parameter
        self._pub.msg.header.identity.id = time.monotonic_ns()
        self._pub.msg.header.identity.api_id = api_id
        self._pub.write()

        try:
            response = self._sub.get(timeout=self.timeout_s)
        except queue.Empty:
            return UT_ROBOT_ERR_CLIENT_API_TIMEOUT, "Request timed out"
        return response.header.status.code, response.data

