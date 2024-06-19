#ifndef _UT_ROBOT_G1_SUBSCRIPTION_WRAPPER_H_
#define _UT_ROBOT_G1_SUBSCRIPTION_WRAPPER_H_

#include <eigen3/Eigen/Dense>
#include "unitree/dds_wrapper/common/Subscription.h"
#include "unitree/dds_wrapper/common/unitree_joystick.hpp"

#include "unitree/idl/x1/LowCmd_hx.hpp"
#include "unitree/idl/x1/LowState_hx.hpp"
#include <unitree/idl/go2/MotorStates_.hpp>

namespace unitree
{
namespace robot
{
namespace g1
{
namespace subscription
{

class LowCmd : public SubscriptionBase<unitree_hx::msg::dds_::LowCmd_>
{
public:
    using SharedPtr = std::shared_ptr<LowCmd>;

    LowCmd(std::string topic = "rt/lowcmd_hx") : SubscriptionBase<MsgType>(topic) {}

private:
    void pre_communication() override
    {
        
    }
};

class LowState : public SubscriptionBase<unitree_hx::msg::dds_::LowState_>
{
public:
    using SharedPtr = std::shared_ptr<LowState>;

    LowState(std::string topic = "rt/lowstate_hx") : SubscriptionBase<MsgType>(topic) {}

    void update()
    {
        std::lock_guard<std::mutex> lock(mutex_);
        // ********** Joystick ********** //
        // 根据当前手柄数值是否全为0 判断手柄是否长时间无操作
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

        // 更新当前的手柄键值
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
    
    // 判断手柄是否长时间无操作
    bool isJoystickTimeout() const  { return isJoystickTimeout_; }
    unitree::common::UnitreeJoystick joystick;

    struct {
        Eigen::Matrix<float, 5, 1> q;
        Eigen::Matrix<float, 5, 1> dq;
        Eigen::Matrix<float, 5, 1> tau;
    } l, r;
    
private:
    void post_communication() override
    {
        for(int i = 0; i < 5; i++)
        {
            l.q[i] = msg_.motor_state()[i+13].q();
            l.dq[i] = msg_.motor_state()[i+13].dq();
            l.tau[i] = msg_.motor_state()[i+13].tau_est();
            r.q[i] = msg_.motor_state()[i+18].q();
            r.dq[i] = msg_.motor_state()[i+18].dq();
            r.tau[i] = msg_.motor_state()[i+18].tau_est();
        }
    }

    uint32_t joystick_timeout_ms_ = 3000;
    bool isJoystickTimeout_ = false;
    std::chrono::time_point<std::chrono::system_clock> last_joystick_time_;
};

class X1Hand : public SubscriptionBase<unitree_go::msg::dds_::MotorStates_>
{
public:
    using SharedPtr = std::shared_ptr<X1Hand>;

    X1Hand(std::string topic = "rt/hand/state") : SubscriptionBase<MsgType>(topic) 
    {
        msg_.states().resize(14);
    }

    struct {
        Eigen::Matrix<float, 7, 1> q;
        Eigen::Matrix<float, 7, 1> dq;
        Eigen::Matrix<float, 7, 1> tau;
    } l, r;

private:
    void post_communication() override
    {
        for(int i = 0; i < 7; i++)
        {
            l.q[i] = msg_.states()[i].q();
            l.dq[i] = msg_.states()[i].dq();
            l.tau[i] = msg_.states()[i].tau_est();
            r.q[i] = msg_.states()[i+7].q();
            r.dq[i] = msg_.states()[i+7].dq();
            r.tau[i] = msg_.states()[i+7].tau_est();
        }
    }
};


} // namespace subscription
} // namespace g1
} // namespace robot
} // namespace unitree


#endif // _UT_ROBOT_G1_SUBSCRIPTION_WRAPPER_H_