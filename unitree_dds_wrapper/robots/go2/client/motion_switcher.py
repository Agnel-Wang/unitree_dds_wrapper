from unitree_dds_wrapper.client import Client
import json

class MotionSwitcherClient(Client):
    def __init__(self):
        super().__init__('motion_switcher')

    def check_mode(self):
        """ 查询当前运行的运控 """
        ret, data = self.call(1001, "")
        return ret, json.loads(data)
    
    def release_mode(self):
        """ 关闭默认运控
        ret: 0 成功
        """
        ret, _ = self.call(1003, "")
        return ret


if __name__ == "__main__":
    import sys
    import argparse
    parser = argparse.ArgumentParser(description="Motion Switcher Client")
    parser.add_argument("-l", "--list", action="store_true", help="List controller")
    parser.add_argument("-r", "--release", action="store_true", help="Release controller")
    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help()
        exit(0)

    client = MotionSwitcherClient()

    ret = 0
    if args.list:
        print(client.check_mode())
    elif args.release:
        print(client.release_mode())