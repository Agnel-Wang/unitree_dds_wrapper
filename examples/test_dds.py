import unitree_dds_wrapper.robots.go2.go2_pub as go2_pub
import unitree_dds_wrapper.robots.go2.go2_sub as go2_sub
import time

pub = go2_pub.LowState()
sub = go2_sub.LowState()

while True:
  pub.msg.level_flag += 1
  pub.write()
  time.sleep(0.5)

  print("send: ", pub.msg.level_flag)

  if sub.msg:
    print("receive: ", sub.msg.level_flag)