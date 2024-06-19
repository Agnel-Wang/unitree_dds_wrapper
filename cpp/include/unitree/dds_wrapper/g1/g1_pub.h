#ifndef _UT_ROBOT_G1_PUBLISHER_WRAPPER_H_
#define _UT_ROBOT_G1_PUBLISHER_WRAPPER_H_

#include <eigen3/Eigen/Dense>
#include <unitree/dds_wrapper/common/Publisher.h>
#include "unitree/dds_wrapper/common/crc.h"

#include <unitree/idl/g1/LowCmd_hx.hpp>
#include <unitree/idl/g1/LowState_hx.hpp>
#include <unitree/idl/go2/MotorCmds_.hpp>


namespace unitree
{
namespace robot
{
namespace g1
{
namespace publisher
{

class LowCmd : public RealTimePublisher<unitree_hx::msg::dds_::LowCmd_>
{
public:
    LowCmd(std::string topic = "rt/lowcmd_hx") : RealTimePublisher<MsgType>(topic) 
    {
        msg_.head() = {0xFE, 0xEF};
        for(auto & m : msg_.motor_cmd()) m.mode(1);
    }

private:
    /**
     * @brief Something before sending the message.
     */
    void pre_communication() override {
        msg_.crc() = crc32_core((uint32_t*)&msg_, (sizeof(MsgType)>>2)-1);
    }
};

class ArmSdk : public RealTimePublisher<unitree_hx::msg::dds_::LowCmd_>
{
public:
    ArmSdk(std::string topic = "rt/arm_sdk") : RealTimePublisher<MsgType>(topic) {}

    struct {
        Eigen::Matrix<float, 5, 1> q;
        Eigen::Matrix<float, 5, 1> dq;
        Eigen::Matrix<float, 5, 1> tau;
    } l, r;

    void setGain(std::array<float, 5> kp, std::array<float, 5> kd)
    {
        for(int i = 0; i < 5; i++)
        {
            msg_.motor_cmd()[i+13].kp() = kp[i];
            msg_.motor_cmd()[i+18].kp() = kd[i];
        }
    }

private:
    void pre_communication() override
    {
        for(int i = 0; i < 5; i++)
        {
            msg_.motor_cmd()[i+13].q() = l.q[i];
            msg_.motor_cmd()[i+13].dq() = l.dq[i];
            msg_.motor_cmd()[i+13].tau() = l.tau[i];
            msg_.motor_cmd()[i+18].q() = r.q[i];
            msg_.motor_cmd()[i+18].dq() = r.dq[i];
            msg_.motor_cmd()[i+18].tau() = r.tau[i];
        }
    }
};

class X1Hand : public RealTimePublisher<unitree_go::msg::dds_::MotorCmds_>
{
public:
    X1Hand(std::string topic = "rt/hand/cmd") : RealTimePublisher<MsgType>(topic) {}

    struct {
        Eigen::Matrix<float, 7, 1> q;
        Eigen::Matrix<float, 7, 1> dq;
        Eigen::Matrix<float, 7, 1> tau;
    } l, r;

    // 左右手相同kp kd; 有可能需要不同
    void setGain(std::array<float, 7> kp, std::array<float, 7> kd)
    {
        for(int i = 0; i < 7; i++)
        {
            msg_.cmds()[i].kp() = kp[i];
            msg_.cmds()[i+7].kp() = kp[i];
        }
    }

private:
    void pre_communication() override
    {
        for(int i = 0; i < 7; i++)
        {
            msg_.cmds()[i].q() = l.q[i];
            msg_.cmds()[i].dq() = l.dq[i];
            msg_.cmds()[i].tau() = l.tau[i];
            msg_.cmds()[i+7].q() = r.q[i];
            msg_.cmds()[i+7].dq() = r.dq[i];
            msg_.cmds()[i+7].tau() = r.tau[i];
        }
    }
};

}; // namespace publisher
}; // namespace g1
}; // namespace robot
}; // namespace unitree

#endif // _UT_ROBOT_G1_PUBLISHER_WRAPPER_H_