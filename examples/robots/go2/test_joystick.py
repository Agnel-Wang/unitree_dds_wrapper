from unitree_dds_wrapper.utils.joystick import SwitchJoystick
import time
from unitree_dds_wrapper.idl import unitree_go


joy = SwitchJoystick()
joy1 = SwitchJoystick()
lowstate = unitree_go.msg.dds_.LowState_()

while True:
    joy.update()
    joy.test()
    joy.print()
    lowstate.wireless_remote = joy.combine()
    joy1.extract(lowstate.wireless_remote)
    print("lx in dds: ", joy1.lx.data)
    print(joy.RT.data)

    time.sleep(0.01)