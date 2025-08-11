from unitree_dds_wrapper.publisher import Publisher
from unitree_dds_wrapper.subscription import Subscription
from unitree_dds_wrapper.idl import unitree_go
import time
from unitree_dds_wrapper.robots import go2


# msg_type = unitree_go.msg.dds_.MotorCmds_
# pub = Publisher(message=msg_type, topic="rt/test_dds")
# sub = Subscription(message=msg_type, topic="rt/test_dds")

pub = go2.pub.MotorCmds(motor_num=2)
sub = go2.sub.MotorCmds()


while True:
  pub.msg.cmds[0].mode = 1 - pub.msg.cmds[0].mode
  pub.write()
  time.sleep(0.5)

  print("send: ", pub.msg.cmds[0].mode)

  if sub.msg:
    print("receive: ", sub.msg.cmds[0].mode)