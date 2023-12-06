import unitree_dds_wrapper.robots.go2.go2_pub as go2_pub
import unitree_dds_wrapper.robots.go2.go2_sub as go2_sub
import time
import unitree_go

motors_states =unitree_go.msg.dds_.MotorStates_()
motors_states.states = [unitree_go.msg.dds_.MotorState_() for _ in range(6)]

lowcmd_pub = go2_pub.LowState()
lowcmd_sub = go2_sub.LowState()

while True:
  lowcmd_pub.msg.level_flag += 1
  lowcmd_pub.write()
  time.sleep(0.5)

  print("send: ", lowcmd_pub.msg.level_flag)

  if lowcmd_sub.msg:
    print("receive: ", lowcmd_sub.msg.level_flag)