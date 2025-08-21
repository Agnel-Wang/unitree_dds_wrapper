from unitree_dds_wrapper.publisher import Publisher
from unitree_dds_wrapper.idl import unitree_hg, unitree_go
from unitree_dds_wrapper.utils.joystick import Joystick
import numpy as np
import struct
from unitree_dds_wrapper.utils.crc import crc32
from unitree_dds_wrapper.robots import g1

class LowCmd(Publisher):
    def __init__(self, participant = None, topic = "rt/lowcmd"):
        super().__init__(unitree_hg.msg.dds_.LowCmd_, topic, participant)
        self.msg: unitree_hg.msg.dds_.LowCmd_
        self.__packCRCformat = '<2B2x' \
         + 'B3x5fI' * len(self.msg.motor_cmd) \
         + '5I'

    def pre_communication(self):
        self.__pack_crc()

    def __pack_crc(self):
        rawdata = []
        rawdata.append(self.msg.mode_pr)
        rawdata.append(self.msg.mode_machine)
        for i in range(len(self.msg.motor_cmd)):
            rawdata.append(self.msg.motor_cmd[i].mode)
            rawdata.append(self.msg.motor_cmd[i].q)
            rawdata.append(self.msg.motor_cmd[i].dq)
            rawdata.append(self.msg.motor_cmd[i].tau)
            rawdata.append(self.msg.motor_cmd[i].kp)
            rawdata.append(self.msg.motor_cmd[i].kd)
            rawdata.append(self.msg.motor_cmd[i].reserve)
        rawdata.extend(self.msg.reserve)
        rawdata.append(self.msg.crc)

        packdata = struct.pack(self.__packCRCformat, *rawdata)
        calcdata = []
        calclen = (len(packdata)>>2)-1
        for i in range(calclen):
            d = ((packdata[i*4+3] << 24) | (packdata[i*4+2] << 16) | (packdata[i*4+1] << 8) | (packdata[i*4]))
            calcdata.append(d)

        self.msg.crc = crc32(calcdata)

class LowState(Publisher):
    def __init__(self, participant = None, topic = "rt/lowstate"):
        super().__init__(unitree_hg.msg.dds_.LowState_, topic, participant)
        self.msg: unitree_hg.msg.dds_.LowState_

class ArmSdk(Publisher):
    def __init__(self, topic: str = "rt/arm_sdk"):
        super().__init__(message=unitree_hg.msg.dds_.LowCmd_, topic=topic)
        self.msg: unitree_hg.msg.dds_.LowCmd_

    @property
    def weight(self):
        return self.msg.motor_cmd[29].q
    
    def Weight(self, w):
        self.msg.motor_cmd[29].q = w

    def SetDefaultGain(self, kp = [40, 40, 40, 40, 40, 40, 40], kd = [1,1,1,1,1,1,1]):
        for i, id in enumerate(g1.LarmJointIndex):
            self.msg.motor_cmd[id].kp = kp[i]
            self.msg.motor_cmd[id].kd = kd[i]
        for i, id in enumerate(g1.RarmJointIndex):
            self.msg.motor_cmd[id].kp = kp[i]
            self.msg.motor_cmd[id].kd = kd[i]

class UnitreeHand(Publisher):
    def __init__(self):
        super().__init__(unitree_go.msg.dds_.MotorCmds_, "rt/hand/cmd")
        self.msg: unitree_go.msg.dds_.MotorCmds_
        self.msg.cmds  = [unitree_go.msg.dds_.MotorCmd_() for _ in range(2 * 7)]