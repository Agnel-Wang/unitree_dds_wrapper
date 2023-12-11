from unitree_z1.msg import dds_
from unitree_dds_wrapper.subscription import Subscription

class MotorCmds(Subscription):
  def __init__(self, participant = None, topic = "rt/z1/lowcmd"):
    super().__init__(dds_.MotorCmds_(), topic, participant)

class MotorStates(Subscription):
  def __init__(self, participant = None, topic = "rt/z1/lowstate"):
    super().__init__(dds_.MotorStates_(), topic, participant)

import geometry_msgs