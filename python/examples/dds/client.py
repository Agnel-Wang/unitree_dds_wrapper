from unitree_dds_wrapper.client import Client
import time

class TeseClient(Client):
    def __init__(self):
        super().__init__("test")

    def test_api(self, parameter = ""):
        ret, data = self.call(1000, parameter)
        print(f"API call returned: {ret}, data: {data}")
        return ret

def main():
    client = TeseClient()
    client.timeout_s = 1.0

    count = 0
    try:
        while True:
            count += 1
            ret = client.test_api(str(count))
            if ret != 0:
                print(f"API call failed with error code: {ret}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Client stopped.")

if __name__ == "__main__":
    main()