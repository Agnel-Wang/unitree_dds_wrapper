from . import h1_pub as pub
from . import h1_sub as sub

from enum import IntEnum

class JointIndex(IntEnum):
    RightHipRoll = 0
    RightHipPitch = 1
    RightKnee = 2
    LeftHipRoll = 3
    LeftHipPitch = 4
    LeftKnee = 5

    WaistYaw = 6
    LeftHipYaw = 7
    RightHipYaw = 8
    # Reserved
    LeftAnkle = 10
    RightAnkle = 11
    RightShoulderPitch = 12
    RightShoulderRoll = 13
    RightShoulderYaw = 14
    RightElbow = 15
    LeftShoulderPitch = 16
    LeftShoulderRoll = 17
    LeftShoulderYaw = 18
    LeftElbow = 19

class LarmJointIndex(IntEnum):
    LeftShoulderPitch = 16
    LeftShoulderRoll = 17
    LeftShoulderYaw = 18
    LeftElbow = 19

class RarmJointIndex(IntEnum):
    RightShoulderPitch = 12
    RightShoulderRoll = 13
    RightShoulderYaw = 14
    RightElbow = 15