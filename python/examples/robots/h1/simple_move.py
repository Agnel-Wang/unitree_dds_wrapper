from unitree_dds_wrapper.robots import h1

robot = h1.simple_controller.H1ArmController()
robot.EnableArmSDK()
robot.LockWaist()
robot.armsdk.MoveJ([0,0,0,0], [0,0,0,0])
robot.EnableArmSDK(False)