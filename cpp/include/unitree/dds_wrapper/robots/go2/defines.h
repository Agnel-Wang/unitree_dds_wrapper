#pragma once

#include <array>

namespace unitree
{
namespace robot
{
namespace go2
{
    
enum class JointIndex{
    FR_Hip = 0,
    FR_Thigh = 1,
    FR_Calf = 2,
    FL_Hip = 3,
    FL_Thigh = 4,
    FL_Calf = 5,
    RR_Hip = 6,
    RR_Thigh = 7,
    RR_Calf = 8,
    RL_Hip = 9,
    RL_Thigh = 10,
    RL_Calf = 11,
};

enum class FSMMode{
    idle = 0,
    balanceStand = 1,
    pose = 2,
    locomotion = 3,
    lieDown = 5,
    jointLock = 6,
    damping = 7,
    recoveryStand = 8,
    sit = 10,
    frontFlip = 11,
    frontJump = 12,
    frontPounc = 13,
};
  
enum class GaitType{
    idle = 0,
    trot = 1,
    run = 2,
    climb_stair = 3,
    forwardDownStair = 4,
    adjust = 9,
};

} // namespace go2
} // namespace robot
} // namespace unitree