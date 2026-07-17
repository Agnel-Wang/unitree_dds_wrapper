from unitree_dds_wrapper.client import Client
import json

class LocoClient(Client):
    def __init__(self):
        super().__init__('sport')
    
    def enable_arm_sdk(self, enable: bool = True):
        parameter = json.dumps({"data": enable})
        ret, _ = self.call(7109, parameter)
        return ret

    def set_fsm_id(self, fsm_id: int):
        parameter = json.dumps({"data": fsm_id})
        ret, _ = self.call(7101, parameter)
        return ret
    

if __name__ == "__main__":
    import sys
    import time
    import argparse
    parser = argparse.ArgumentParser(description="G1 Loco Client")
    parser.add_argument('--set_fsm_id', type=int, help='Set FSM ID')
    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help()
        exit(0)
    ret = 0

    client = LocoClient()

    if args.set_fsm_id is not None:
        ret = client.set_fsm_id(args.set_fsm_id)
        print(f"Set FSM ID result: {ret}")