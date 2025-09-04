from unitree_dds_wrapper.server import Server
import time
import asyncio
from typing import Tuple

class TestServer(Server):
    def __init__(self):
        super().__init__("test")
        self.register(1000, self.sync_handler)
        self.register(1001, self.async_handler)

    def sync_handler(self, parameter: str) -> Tuple[int, str]:
        print(f"Received parameter: {parameter}")
        time.sleep(1)
        return 0, f"Response for {parameter}"
    
    async def async_handler(self, parameter: str) -> Tuple[int, str]:
        print(f"Async handler received parameter: {parameter}")
        await asyncio.sleep(1)
        return 0, f"Async response for {parameter}"

def main():
    server = TestServer()
    server.start()

    print("Server started. Waiting for requests...")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Server stopped.")

if __name__ == "__main__":
    main()