import unitree_dds_wrapper.robots.go2.go2_pub as go2_pub
import time
from cyclonedds.domain import DomainParticipant

participant = DomainParticipant(domain_id=1)
lowcmd = go2_pub.LowCmd(participant)

pos = [0, 0.67, -1.3]
for i in range(12):
  lowcmd.msg.motor_cmd[i].kp = 60
  lowcmd.msg.motor_cmd[i].kd = 5
  lowcmd.msg.motor_cmd[i].q = pos[i % 3]

while True:
  lowcmd.write()
  time.sleep(0.5)