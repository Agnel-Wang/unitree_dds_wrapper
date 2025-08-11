from unitree_dds_wrapper.idl.unitree_api.msg import dds_
from unitree_dds_wrapper.publisher import Publisher
from unitree_dds_wrapper.subscription import Subscription
import queue
from typing import Callable
from threading import Thread


class RequestSubscriber(Subscription):
    def __init__(self, topic):
        super().__init__(dds_.Request_, topic)
        self._queue = queue.Queue(10)
        
    def post_communication(self):
        self._queue.put(self.msg)

    def get(self) -> dds_.Request_:
        return self._queue.get(block=True)
    
class ResponsePublisher(Publisher):
    def __init__(self, topic):
        super().__init__(dds_.Response_, topic)
        self.msg: dds_.Response_

class Server:
    def __init__(self, name: str):
        self._pub = ResponsePublisher(topic=f"rt/api/{name}/response")
        self._sub = RequestSubscriber(topic=f"rt/api/{name}/request")
        self._handlers = {}

    def start(self):
        self._thread = Thread(target=self._run, daemon=True)
        self._thread.start()

    # handler: [](str) -> (int, str)
    def register(self, api_id: int, handler: Callable):
        if api_id in self._handlers:
            raise ValueError(f"Handler for ID {api_id} already registered.")
        self._handlers[api_id] = handler

    def _run(self):
        while True:
            request = self._sub.get()
            api_id = request.header.identity.api_id
            if api_id in self._handlers:
                ret, response = self._handlers[api_id](request.parameter)
                self._pub.msg.data = response
                self._pub.msg.header.identity.id = request.header.identity.id
                self._pub.msg.header.identity.api_id = api_id
                self._pub.msg.header.status.code = ret
                self._pub.write()
