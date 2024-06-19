#ifndef _UT_ROBOT_G1_H__ // 多添加一个 _ 防止和G1原本的头文件冲突
#define _UT_ROBOT_G1_H__

#include <unitree/dds_wrapper/g1/g1_pub.h>
#include <unitree/dds_wrapper/g1/g1_sub.h>

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
    LeftAnkle = 4,
    LeftAnkleRoll = 5,

    // Right leg
    RightHipPitch = 6,
    RightHipRoll = 7,
    RightHipYaw = 8,
    RightKnee = 9,
    RightAnkle = 10,
    RightAnkleRoll = 11,

    WaistYaw = 12,

    // Left arm
    LeftShoulderPitch = 13,
    LeftShoulderRoll = 14,
    LeftShoulderYaw = 15,
    LeftElbow = 16,
    LeftWrist = 17,

    // Right arm
    RightShoulderPitch = 18,
    RightShoulderRoll = 19,
    RightShoulderYaw = 20,
    RightElbow = 21,
    RightWrist = 22,
};

} // namespace g1
} // namespace robot
} // namespace unitree

#endif // _UT_ROBOT_G1_H__