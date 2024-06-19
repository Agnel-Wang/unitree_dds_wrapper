from unitree_dds_wrapper.utils.joystick import LogicJoystick
import time

joy = LogicJoystick()

while True:
    joy.update()
    print(joy.lx.data)
    time.sleep(0.1)
