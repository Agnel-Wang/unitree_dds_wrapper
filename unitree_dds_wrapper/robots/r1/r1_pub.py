from unitree_dds_wrapper.publisher import Publisher
from unitree_dds_wrapper.idl import unitree_hg, unitree_go
import numpy as np

class ArmSdk(Publisher):
    def __init__(self, topic: str = "rt/arm_sdk"):
        super().__init__(message=unitree_hg.msg.dds_.LowCmd_, topic=topic)
        self.msg: unitree_hg.msg.dds_.LowCmd_

    # different from g1, r1 use mode_pr to control weight, 
    # g1 use motor_cmd[29].q to control weight
    @property
    def weight(self):
        return float(self.msg.mode_pr) / 100.0
    
    @weight.setter
    def weight(self, w):
        self.msg.mode_pr = int(np.clip(w * 100, 0, 100))
