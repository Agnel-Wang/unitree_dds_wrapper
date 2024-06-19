#ifndef _UT_ROBOT_GO2_PUBLISHER_WRAPPER_H_
#define _UT_ROBOT_GO2_PUBLISHER_WRAPPER_H_

#include "unitree/dds_wrapper/common/Publisher.h"
#include "unitree/dds_wrapper/common/crc.h"

#include <unitree/idl/go2/LowCmd_.hpp>
#include <unitree/idl/go2/LowState_.hpp>
#include <unitree/idl/go2/SportModeCmd_.hpp>
#include <unitree/idl/go2/SportModeState_.hpp>
#include <unitree/idl/go2/LidarState_.hpp>
#include <unitree/idl/go2/UwbState_.hpp>
#include <unitree/idl/go2/HeightMap_.hpp>
#include <unitree/idl/ros2/Time_.hpp>
#include <unitree/idl/ros2/PointCloud2_.hpp>
#include <unitree/idl/go2/WirelessController_.hpp>
#include <unitree/idl/go2/Res_.hpp>
#include <unitree/idl/go2/MotorCmds_.hpp>
#include <unitree/idl/go2/MotorStates_.hpp>


namespace unitree
{
namespace robot
{
namespace go2
{ 
namespace publisher
{

class LowCmd : public RealTimePublisher<unitree_go::msg::dds_::LowCmd_>
{
public:
  LowCmd(std::string topic = "rt/lowcmd")
  : RealTimePublisher<MsgType>(topic) 
  {
    msg_.head() = {0xFE, 0xEF};
    msg_.level_flag() = 0xFF;

    for (auto & m : msg_.motor_cmd()) m.mode(1);
  } 

private:
  /**
   * @brief Something before sending the message.
   */
  void pre_communication() override {
    msg_.crc() = crc32_core((uint32_t*)&msg_, (sizeof(MsgType)>>2)-1);
  }
};


class LowState : public RealTimePublisher<unitree_go::msg::dds_::LowState_>
{
public:
  LowState(std::string topic = "rt/lowstate")
  : RealTimePublisher<MsgType>(topic) 
  {}
};

class MotorCmds : public RealTimePublisher<unitree_go::msg::dds_::MotorCmds_>
{
public:
  MotorCmds(std::string topic)
  : RealTimePublisher<MsgType>(topic) 
  {}
};

class MotorStates : public RealTimePublisher<unitree_go::msg::dds_::MotorStates_>
{
public:
  MotorStates(std::string topic)
  : RealTimePublisher<MsgType>(topic) 
  {}
};

} // namespace publisher
} // namespace go2
} // namespace robot
} // namespace unitree

#endif // _UT_ROBOT_GO2_PUBLISHER_WRAPPER_H_