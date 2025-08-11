#pragma once

#include <array>

namespace unitree
{
namespace robot
{
namespace g1
{

enum JointIndex{
    // Left leg
    LeftHipPitch = 0,
    LeftHipRoll = 1,
    LeftHipYaw = 2,
    LeftKnee = 3,
    LeftAnklePitch = 4,
    LeftAnkleRoll = 5,

    // Right leg
    RightHipPitch = 6,
    RightHipRoll = 7,
    RightHipYaw = 8,
    RightKnee = 9,
    RightAnklePitch = 10,
    RightAnkleRoll = 11,

    WaistYaw = 12,
    WaistRoll = 13,
    WaistPitch = 14,

    // Left arm
    LeftShoulderPitch = 15,
    LeftShoulderRoll = 16,
    LeftShoulderYaw = 17,
    LeftElbow = 18,
    LeftWristRoll = 19,
    LeftWristPitch = 20,
    LeftWristYaw = 21,

    // Right arm
    RightShoulderPitch = 22,
    RightShoulderRoll = 23,
    RightShoulderYaw = 24,
    RightElbow = 25,
    RightWristRoll = 26,
    RightWristPitch = 27,
    RightWristYaw = 28
};

static const std::array<int, 29> JointIndexArray = {
    LeftHipPitch,  LeftHipRoll,  LeftHipYaw,  LeftKnee,
    LeftAnklePitch, LeftAnkleRoll,
    RightHipPitch, RightHipRoll, RightHipYaw, RightKnee,
    RightAnklePitch, RightAnkleRoll,
    WaistYaw, WaistRoll, WaistPitch,
    LeftShoulderPitch, LeftShoulderRoll,
    LeftShoulderYaw, LeftElbow,
    LeftWristRoll, LeftWristPitch,
    LeftWristYaw,
    RightShoulderPitch, RightShoulderRoll,
    RightShoulderYaw, RightElbow,
    RightWristRoll, RightWristPitch,
    RightWristYaw
};

static const std::array<int, 17> ArmJoints = {
    JointIndex::LeftShoulderPitch,  JointIndex::LeftShoulderRoll,
    JointIndex::LeftShoulderYaw,    JointIndex::LeftElbow,
    JointIndex::LeftWristRoll,       JointIndex::LeftWristPitch,
    JointIndex::LeftWristYaw,
    JointIndex::RightShoulderPitch, JointIndex::RightShoulderRoll,
    JointIndex::RightShoulderYaw,   JointIndex::RightElbow,
    JointIndex::RightWristRoll,      JointIndex::RightWristPitch,
    JointIndex::RightWristYaw,
    JointIndex::WaistYaw,
    JointIndex::WaistRoll,
    JointIndex::WaistPitch
};

enum MachineType {
    unknown,
    dof14,
    dof23,
    dof29
};

enum HandType {
    None,
    Dex3,
    Inspire
};


} // namespace g1
} // namespace robot
} // namespace unitree