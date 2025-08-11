#pragma once

#include <eigen3/Eigen/Dense>
#include "unitree/dds_wrapper/common/Subscription.h"
#include "unitree/dds_wrapper/common/unitree_joystick.hpp"
#include "defines.h"

#include <unitree/idl/hg/LowCmd_.hpp>
#include <unitree/idl/hg/LowState_.hpp>
#include <unitree/idl/hg/HandCmd_.hpp>
#include <unitree/idl/hg/HandState_.hpp>
#include <unitree/idl/hg/SportModeState_.hpp>
#include <unitree/idl/go2/MotorStates_.hpp>

namespace unitree
{
namespace robot
{
namespace g1
{
namespace subscription
{

class LowCmd : public SubscriptionBase<unitree_hg::msg::dds_::LowCmd_>
{
public:
    using SharedPtr = std::shared_ptr<LowCmd>;

    LowCmd(std::string topic = "rt/lowcmd") : SubscriptionBase<MsgType>(topic) {}

};

class ArmSdk : public SubscriptionBase<unitree_hg::msg::dds_::LowCmd_>
{
public:
    using SharedPtr = std::shared_ptr<LowCmd>;

    ArmSdk(std::string topic = "rt/arm_sdk") : SubscriptionBase<MsgType>(topic) {}

};
class LowState : public SubscriptionBase<unitree_hg::msg::dds_::LowState_>
{
public:
    using SharedPtr = std::shared_ptr<LowState>;

    LowState(std::string topic = "rt/lowstate") : SubscriptionBase<MsgType>(topic) {}

    MachineType machine_type() const
    {
        // 暂时忽略锁腰
        switch(msg_.mode_machine())
        {
            // case 0:
            case 1:
            case 4:
                return MachineType::dof23;
            case 2:
            case 3:
            case 5:
            case 6:
                return MachineType::dof29;
            case 9:
                return MachineType::dof14;
        }
        return MachineType::unknown;
    }

    void update()
    {
        std::lock_guard<std::mutex> lock(mutex_);
        // ********** Joystick ********** //
        // Check if all joystick values are zero to determine if the joystick is inactive
        if(std::all_of(msg_.wireless_remote().begin(), msg_.wireless_remote().end(), [](uint8_t i){return i == 0;}))
        {
            auto now = std::chrono::system_clock::now();
            auto elasped_time = now - last_joystick_time_;
            if(elasped_time > std::chrono::milliseconds(joystick_timeout_ms_))
            {
                isJoystickTimeout_ = true;
            }
        } else {
            last_joystick_time_ = std::chrono::system_clock::now();
            isJoystickTimeout_ = false;
        }

        // update joystick state
        unitree::common::REMOTE_DATA_RX key;
        memcpy(&key, &msg_.wireless_remote()[0], 40);
        joystick.back(key.RF_RX.btn.components.Select);
        joystick.start(key.RF_RX.btn.components.Start);
        joystick.LB(key.RF_RX.btn.components.L1);
        joystick.RB(key.RF_RX.btn.components.R1);
        joystick.F1(key.RF_RX.btn.components.f1);
        joystick.F2(key.RF_RX.btn.components.f2);
        joystick.A(key.RF_RX.btn.components.A);
        joystick.B(key.RF_RX.btn.components.B);
        joystick.X(key.RF_RX.btn.components.X);
        joystick.Y(key.RF_RX.btn.components.Y);
        joystick.up(key.RF_RX.btn.components.up);
        joystick.down(key.RF_RX.btn.components.down);
        joystick.left(key.RF_RX.btn.components.left);
        joystick.right(key.RF_RX.btn.components.right);
        joystick.LT(key.RF_RX.btn.components.L2);
        joystick.RT(key.RF_RX.btn.components.R2);
        joystick.lx(key.RF_RX.lx);
        joystick.ly(key.RF_RX.ly);
        joystick.rx(key.RF_RX.rx);
        joystick.ry(key.RF_RX.ry);
    }
    
    bool isJoystickTimeout() const  { return isJoystickTimeout_; }
    unitree::common::UnitreeJoystick joystick;
    
private:
    uint32_t joystick_timeout_ms_ = 3000;
    bool isJoystickTimeout_ = false;
    std::chrono::time_point<std::chrono::system_clock> last_joystick_time_;
};

class InspireHandState : public SubscriptionBase<unitree_go::msg::dds_::MotorStates_>
{
public:
    using SharedPtr = std::shared_ptr<InspireHandState>;

    InspireHandState(std::string topic = "rt/inspire/state") : SubscriptionBase<MsgType>(topic) {}
};

class Dex3LeftHandState : public SubscriptionBase<unitree_hg::msg::dds_::HandState_>
{
public:
    using SharedPtr = std::shared_ptr<Dex3LeftHandState>;

    Dex3LeftHandState(std::string topic = "rt/dex3/left/state") : SubscriptionBase<MsgType>(topic) {}
};

class Dex3RightHandState : public SubscriptionBase<unitree_hg::msg::dds_::HandState_>
{
public:
    using SharedPtr = std::shared_ptr<Dex3RightHandState>;

    Dex3RightHandState(std::string topic = "rt/dex3/right/state") : SubscriptionBase<MsgType>(topic) {}
};

} // namespace subscription
} // namespace g1
} // namespace robot
} // namespace unitree