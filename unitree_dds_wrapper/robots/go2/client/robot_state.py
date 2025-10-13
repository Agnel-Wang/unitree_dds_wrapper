from unitree_dds_wrapper.client import Client
import json

class RobotState(Client):
    def __init__(self):
        super().__init__('robot_state')

    def service_list(self) -> list:
        ret, data = self.call(1003, "")
        return json.loads(data)

if __name__ == "__main__":
    import sys
    import argparse
    parser = argparse.ArgumentParser(description="G1 Arm Client")
    parser.add_argument("-l", "--list", action="store_true", help="List service status")
    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help()
        exit(0)

    client = RobotState()

    ret = 0
    if args.list:
        print(client.service_list())