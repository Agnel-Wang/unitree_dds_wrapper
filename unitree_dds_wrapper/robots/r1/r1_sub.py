from unitree_dds_wrapper.idl import unitree_hg, unitree_go
from unitree_dds_wrapper.subscription import Subscription
from unitree_dds_wrapper.utils.joystick import Joystick

class ArmSdk(Subscription):
    """可用于判断当前是否有程序在控制上肢
    默认不自动读取消息, 需要时调用take_one()更新
    """
    def __init__(self, participant = None, topic: str = "rt/arm_sdk", autospin=False):
        super().__init__(unitree_hg.msg.dds_.LowCmd_, topic=topic, participant=participant, autospin=autospin)
        self.msg: unitree_go.msg.dds_.LowCmd_

    @property
    def weight(self):
        return float(self.msg.mode_pr) / 100.0