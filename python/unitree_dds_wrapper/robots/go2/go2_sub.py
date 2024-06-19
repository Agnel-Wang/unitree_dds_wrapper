from unitree_dds_wrapper.idl.unitree_go.msg import dds_
from unitree_dds_wrapper.subscription import Subscription
from unitree_dds_wrapper.utils.joystick import Joystick
import struct

class LowCmd(Subscription):
  def __init__(self, participant = None, topic: str = "rt/lowcmd"):
    super().__init__(dds_.LowCmd_, topic=topic, participant=participant)

class LowState(Subscription):
  def __init__(self, participant = None, topic: str = "rt/lowstate"):
    super().__init__(dds_.LowState_, topic=topic, participant=participant)
    self.joystick = Joystick()

  def update(self):
    """
    根据当前的lowstate提取相应信息
    """
    if self.msg is None:
      return

    # Joystick
    # Buttons
    button1 = [int(data) for data in f'{self.msg.wireless_remote[2]:08b}']
    button2 = [int(data) for data in f'{self.msg.wireless_remote[3]:08b}']
    self.joystick.LT(button1[2])
    self.joystick.RT(button1[3])
    self.joystick.back(button1[4])
    self.joystick.start(button1[5])
    self.joystick.LB(button1[6])
    self.joystick.RB(button1[7])
    self.joystick.left(button2[0])    
    self.joystick.down(button2[1])
    self.joystick.right(button2[2])
    self.joystick.up(button2[3])
    self.joystick.Y(button2[4])
    self.joystick.X(button2[5])
    self.joystick.B(button2[6])
    self.joystick.A(button2[7])
    # Axes
    self.joystick.lx( struct.unpack('f', bytes(self.msg.wireless_remote[4:8]))[0] )
    self.joystick.rx( struct.unpack('f', bytes(self.msg.wireless_remote[8:12]))[0] )
    self.joystick.ry( struct.unpack('f', bytes(self.msg.wireless_remote[12:16]))[0] )
    self.joystick.ly( struct.unpack('f', bytes(self.msg.wireless_remote[20:24]))[0] )

class MotorStates(Subscription):
  def __init__(self, participant = None, topic: str = "rt/motor_states"):
    super().__init__(dds_.MotorStates_, topic=topic, participant=participant)

class MotorCmds(Subscription):
  def __init__(self, participant = None, topic: str = "rt/motor_cmds"):
    super().__init__(dds_.MotorCmds_, topic=topic, participant=participant)
