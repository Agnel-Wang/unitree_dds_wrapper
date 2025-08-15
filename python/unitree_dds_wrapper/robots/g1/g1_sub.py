from unitree_dds_wrapper.idl import unitree_hg, unitree_go
from unitree_dds_wrapper.subscription import Subscription
from unitree_dds_wrapper.utils.joystick import Joystick

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
        """
        根据当前的lowstate提取相应信息
        """
        if self.msg is None:
            return

        with self.lock:    
            self.joystick.extract(self.msg.wireless_remote)

class ArmSdk(Subscription):
    def __init__(self, participant = None, topic: str = "rt/armsdk"):
        super().__init__(unitree_go.msg.dds_.LowCmd_, topic=topic, participant=participant)
        self.msg: unitree_go.msg.dds_.LowCmd_

    @property
    def weight(self):
        return self.msg.motor_cmd[29].q

class SportModeState(Subscription):
    def __init__(self, participant = None, topic: str = "rt/sportmodestate"):
        super().__init__(unitree_hg.msg.dds_.SportModeState_, topic=topic, participant=participant)
        self.msg: unitree_hg.msg.dds_.SportModeState_