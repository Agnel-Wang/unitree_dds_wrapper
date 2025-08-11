from unitree_dds_wrapper.server import Server
import time

class TestServer(Server):
    def __init__(self):
        super().__init__("test")
        self.register(1000, self.test_callback)

    def test_callback(self, parameter: str) -> tuple[int, str]:
        print(f"Received parameter: {parameter}")

        return 0, f"Response for {parameter}"
    
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