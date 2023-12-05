from unitree_go.msg import dds_
from unitree_dds_wrapper.subscription import Subscription
from unitree_go.dds_helper import *

class LowCmd(Subscription):
  def __init__(self, participant = None):
    super().__init__(dds_.LowCmd_, "rt/lowcmd", participant)

class LowState(Subscription):
  def __init__(self, participant = None):
    super().__init__(dds_.LowState_, "rt/lowstate", participant)