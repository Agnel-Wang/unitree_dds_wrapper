from unitree_dds_wrapper.idl.unitree_api.msg import dds_
from unitree_dds_wrapper.publisher import Publisher
from unitree_dds_wrapper.subscription import Subscription
import queue
from typing import Callable
from threading import Thread

import asyncio
from concurrent.futures import ThreadPoolExecutor

UT_ROBOT_ERR_CLIENT_API_NOT_REG = 3103
UT_ROBOT_ERR_SERVER_INTERNAL = 3202

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
        self._loop = asyncio.new_event_loop()
        self._executor = ThreadPoolExecutor(max_workers=4)

    def start(self):
        # 启动 asyncio 事件循环线程
        self._thread = Thread(target=self._loop.run_forever, daemon=True)
        self._thread.start()
        # 启动 DDS 监听线程
        self._listen_thread = Thread(target=self._run, daemon=True)
        self._listen_thread.start()

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
                ret, response = await handler(request.parameter)
            else:
                ret, response = await self._loop.run_in_executor(
                    self._executor, handler, request.parameter
                )
        except Exception as e:
            ret, response = -1, str(e)

        msg = dds_.Response_()
        msg.data = response
        msg.header.identity.id = request.header.identity.id
        msg.header.identity.api_id = api_id
        msg.header.status.code = ret
        self._pub.write(msg)