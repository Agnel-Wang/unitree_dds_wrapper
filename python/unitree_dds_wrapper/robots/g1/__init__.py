from . import g1_pub as pub
from . import g1_sub as sub

from enum import IntEnum

class JointIndex(IntEnum):
    # Left leg
    LeftHipPitch = 0
    LeftHipRoll = 1
    LeftHipYaw = 2
    LeftKnee = 3
    LeftAnkle = 4
    LeftAnkleRoll = 5

    # Right leg
    RightHipPitch = 6
    RightHipRoll = 7
    RightHipYaw = 8
    RightKnee = 9
    RightAnkle = 10
    RightAnkleRoll = 11

    WaistYaw = 12

    # Left arm
    LeftShoulderPitch = 13
    LeftShoulderRoll = 14
    LeftShoulderYaw = 15
    LeftElbow = 16
    LeftWrist = 17

    # Right arm
    RightShoulderPitch = 18
    RightShoulderRoll = 19
    RightShoulderYaw = 20
    RightElbow = 21
    RightWrist = 22

__all__ = ['pub', 'sub', 'JointIndex']
