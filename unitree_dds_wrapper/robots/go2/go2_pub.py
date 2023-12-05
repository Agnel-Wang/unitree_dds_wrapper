from unitree_go.msg import dds_
from unitree_dds_wrapper.publisher import Publisher
class LowCmd(Publisher):
  def __init__(self, participant = None):
    super().__init__(dds_.LowCmd_, "rt/lowcmd", participant)
    self.msg = dds_.LowCmd_()

class LowState(Publisher):
  def __init__(self, participant = None):
    super().__init__(dds_.LowState_, "rt/lowstate", participant)
    self.msg = dds_.LowState_()