from unitree_dds_wrapper.publisher import Publisher
from unitree_dds_wrapper.idl import unitree_go
import numpy as np

class ArmSdk(Publisher):
    def __init__(self):
        super().__init__(message=unitree_go.msg.dds_.LowCmd_, topic="rt/arm_sdk")
        self.msg = unitree_go.msg.dds_.LowCmd_()
        self.msg.motor_cmd[9].q = 1 # weight

        class ArmCmd:
            def __init__(self):
                self.kp: np.array = np.zeros(4)
                self.kd: np.array = np.zeros(4)
                self.q: np.array = np.zeros(4)
                self.dq: np.array = np.zeros(4)
                self.tau: np.array = np.zeros(4)

        self.l = ArmCmd()
        self.r = ArmCmd()
        self.waist = self.msg.motor_cmd[6]

    def pre_communication(self):
        for i in range(4):
            for attr in ["kp", "kd", "q", "dq", "tau"]:
                setattr(self.msg.motor_cmd[i + 12], attr, getattr(self.r, attr)[i])
                setattr(self.msg.motor_cmd[i + 16], attr, getattr(self.l, attr)[i])

class InspireHand(Publisher):
    def __init__(self):
        super().__init__(unitree_go.msg.dds_.MotorCmds_, "rt/inspire/cmd")
        self.msg.cmds  = [unitree_go.msg.dds_.MotorCmd_() for _ in range(12)]

        self.labels = {}
        self.labels["open"] = np.ones(6)
        self.labels["close"] = np.zeros(6)

        self.lq = np.zeros(6)
        self.rq = np.zeros(6)

    def pre_communication(self):
        for i in range(6):
            self.msg.cmds[i].q = self.lq[i]
            self.msg.cmds[i+6].q = self.rq[i]

    def ctrl(self, label):
        try:
            self.lq = self.labels[label]
            self.rq = self.labels[label]
            self.write()
        except :
            print(f"label {label} not found")