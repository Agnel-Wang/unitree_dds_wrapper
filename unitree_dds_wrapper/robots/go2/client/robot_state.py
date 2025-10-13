from unitree_dds_wrapper.client import Client
from enum import IntEnum
import json


class StatusCode(IntEnum):
    SUCCESS = 0
    ERROR_COMMON = 5201
    ERROR_PROTECTED = 5202

class RobotState(Client):
    def __init__(self):
        super().__init__('robot_state')

    def service_list(self):
        ret, data = self.call(1003, "")
        if ret != 0:
            return None
        return json.loads(data)

    def service_switch(self, name: str, switch: int):
        """ 切换服务状态
        name: 服务名称
        switch: 目标状态 0 关闭 1 打开
        status: 当前状态 0 开启 1 关闭 , 虽然很困惑 但确实是这样的
        ret: 0 成功
        """
        req = {
            "name": name,
            "switch": switch,
        }
        ret, data = self.call(1001, json.dumps(req))
        data = json.loads(data)
        if ret == 0:
            if data["status"] == 5:
                return StatusCode.ERROR_PROTECTED
            if data["status"] != 0 and data["status"] != 1:
                return StatusCode.ERROR_COMMON
        return ret


if __name__ == "__main__":
    import sys
    import argparse
    parser = argparse.ArgumentParser(description="G1 Arm Client")
    parser.add_argument("-l", "--list", action="store_true", help="List service status")
    parser.add_argument("-s", "--switch", nargs=2, metavar=('name', 'switch'), help="Switch service status")
    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help()
        exit(0)

    client = RobotState()

    ret = 0
    if args.list:
        print(client.service_list())
    elif args.switch is not None:
        name, switch = args.switch
        data = client.service_list()
        module = None
        if data is None:
            print("Failed to get service list.")
            exit(1)
        for _ in data:
            if _["name"] == name:
                module = _
                break
        if module is None:
            print(f"Service {name} not found.")
            exit(1)

        print(f"Current {name} status: ", module["status"])
        ret = client.service_switch(name, int(switch))
        print(f"Switch service {name} to {switch}, ret: {ret}")