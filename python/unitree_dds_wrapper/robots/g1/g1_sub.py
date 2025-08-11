from unitree_dds_wrapper.idl import unitree_hg, unitree_go
from unitree_dds_wrapper.subscription import Subscription
from unitree_dds_wrapper.utils.joystick import Joystick
import numpy as np

class LowCmd(Subscription):
    def __init__(self, participant = None, topic: str = "rt/lowcmd"):
        super().__init__(unitree_hg.msg.dds_.LowCmd_, topic=topic, participant=participant)
        self.msg: unitree_hg.msg.dds_.LowCmd_

class LowState(Subscription):
    def __init__(self, participant = None, topic: str = "rt/lowstate"):
        super().__init__(unitree_hg.msg.dds_.LowState_, topic=topic, participant=participant)
        self.msg: unitree_hg.msg.dds_.LowState_
        self.joystick = Joystick()

    def update(self):
        if self.msg is None:
            return

        with self.lock:    
            self.joystick.extract(self.msg.wireless_remote)


class UnitreeHand(Subscription):
    def __init__(self):
        super().__init__(unitree_go.msg.dds_.MotorStates_, "rt/hand/state")
        # self.msg.states = [unitree_go.msg.dds_.MotorState_() for _ in range(2 * 7)]
