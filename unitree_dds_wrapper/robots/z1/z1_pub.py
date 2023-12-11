from unitree_z1.msg import dds_
from unitree_dds_wrapper.publisher import Publisher

class MotorCmds(Publisher):
  def __init__(self, participant = None, topic = "rt/z1/lowcmd"):
    super().__init__(dds_.MotorCmds_, topic, participant)
    self.msg = dds_.MotorCmds_()
    self.msg.cmds = [dds_.MotorCmd_() for _ in range(7)]

class MotorStates(Publisher):
  def __init__(self, participant = None, topic = "rt/z1/lowstate"):
    super().__init__(dds_.MotorStates_, topic, participant)
    self.msg = dds_.MotorStates_()
    self.msg.states = [dds_.MotorState_() for _ in range(7)]