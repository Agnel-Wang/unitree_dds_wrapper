from unitree_dds_wrapper.utils.joystick import LogicJoystick, GameSirJoystick
import time
from unitree_dds_wrapper.idl import unitree_go


joy = GameSirJoystick()
joy1 = GameSirJoystick()
lowstate = unitree_go.msg.dds_.LowState_()

while True:
    joy.update()
    joy.test()
    joy.print()
    lowstate.wireless_remote = joy.combine()
    joy1.extract(lowstate.wireless_remote)
    print("lx in dds: ", joy1.lx.data)

    time.sleep(0.01)