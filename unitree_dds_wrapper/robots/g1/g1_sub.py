from unitree_dds_wrapper.idl import unitree_hg, unitree_go
from unitree_dds_wrapper.subscription import Subscription
from unitree_dds_wrapper.utils.joystick import Joystick

class LowCmd(Subscription):
    def __init__(self, participant = None, topic: str = "rt/lowcmd", autospin=True):
        super().__init__(unitree_hg.msg.dds_.LowCmd_, topic=topic, participant=participant, autospin=autospin)
        self.msg: unitree_hg.msg.dds_.LowCmd_

class LowState(Subscription):
    def __init__(self, participant = None, topic: str = "rt/lowstate", autospin=True):
        super().__init__(unitree_hg.msg.dds_.LowState_, topic=topic, participant=participant, autospin=autospin)
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
    """可用于判断当前是否有程序在控制上肢
    默认不自动读取消息, 需要时调用take_one()更新
    """
    def __init__(self, participant = None, topic: str = "rt/armsdk", autospin=False):
        super().__init__(unitree_hg.msg.dds_.LowCmd_, topic=topic, participant=participant, autospin=autospin)
        self.msg: unitree_go.msg.dds_.LowCmd_

    @property
    def weight(self):
        return self.msg.motor_cmd[29].q

class SportModeState(Subscription):
    """
    用于根据当前G1的运动模式状态进行相应判断
    默认不自动读取消息, 需要时调用take_one()更新
    """
    def __init__(self, participant = None, topic: str = "rt/sportmodestate", autospin=False):
        super().__init__(unitree_hg.msg.dds_.SportModeState_, topic=topic, participant=participant, autospin=autospin)
        self.msg: unitree_hg.msg.dds_.SportModeState_


class BmsState(Subscription):
    """
    用于获取G1的电池状态
    """
    def __init__(self, participant = None, topic: str = "rt/lf/bmsstate", autospin=True):
        super().__init__(unitree_hg.msg.dds_.BmsState_, topic=topic, participant=participant, autospin=autospin)
        self.msg: unitree_hg.msg.dds_.BmsState_