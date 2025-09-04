from unitree_dds_wrapper.client import Client
import json

class LocoClient(Client):
    def __init__(self):
        super().__init__('sport')
    
    def enable_arm_sdk(self, enable: bool = True):
        parameter = json.dumps({"data": enable})
        ret, _ = self.call(7109, parameter)
        return ret
        
