from unitree_dds_wrapper.robots import h1

cmd = h1.pub.DamiaoWristCmd()
state = h1.sub.DamiaoWristState()
print("等待手腕服务启动")
state.wait_for_connection()
for i in range(2):
    cmd.msg.cmds[i].q = state.msg.states[i].q

print("移动手腕到指定角度")
cmd.move([1, 1])