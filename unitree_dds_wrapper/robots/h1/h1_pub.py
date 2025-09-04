from unitree_dds_wrapper.publisher import Publisher
from unitree_dds_wrapper.idl import unitree_go
from unitree_dds_wrapper.robots import h1
from scipy import interpolate as si
import numpy as np
import time

class LowCmd(Publisher):
    def __init__(self, topic = "rt/lowcmd"):
        super().__init__(message=unitree_go.msg.dds_.LowCmd_, topic=topic)
        self.msg: unitree_go.msg.dds_.LowCmd_

class ArmSdk(Publisher):
    def __init__(self, topic = "rt/arm_sdk"):
        super().__init__(message=unitree_go.msg.dds_.LowCmd_, topic=topic)
        self.msg: unitree_go.msg.dds_.LowCmd_
        self.Weight(1)

    def Weight(self, weight):
        self.msg.motor_cmd[9].q = weight

class InspireHand(Publisher):
    def __init__(self):
        super().__init__(unitree_go.msg.dds_.MotorCmds_, "rt/inspire/cmd")
        self.msg.cmds  = [unitree_go.msg.dds_.MotorCmd_() for _ in range(12)]

class DamiaoWristCmd(Publisher):
    def __init__(self):
        super().__init__(unitree_go.msg.dds_.MotorCmds_, "rt/wrist/cmd")
        self.msg: unitree_go.msg.dds_.MotorCmds_
        self.msg.cmds  = [unitree_go.msg.dds_.MotorCmd_() for _ in range(2)]