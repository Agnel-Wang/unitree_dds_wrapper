#ifndef _UT_ROBOT_GO2_PUBLISHER_WRAPPER_H_
#define _UT_ROBOT_GO2_PUBLISHER_WRAPPER_H_

#include "unitree_dds_wrapper/common/Publisher.h"
#include "unitree_dds_wrapper/common/crc.h"

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

namespace unitree
{
namespace robot
{
namespace go2
{ 
namespace publisher
{

class LowCmd : public PublisherBase<unitree_go::msg::dds_::LowCmd_>
{
public:
  LowCmd() : PublisherBase<MsgType>("rt/lowcmd") {}
};

class RealTimeLowCmd : public RealTimePublisher<unitree_go::msg::dds_::LowCmd_>
{
public:
  RealTimeLowCmd(PublisherSharedPtr publisher = std::make_shared<LowCmd>())
  : RealTimePublisher<unitree_go::msg::dds_::LowCmd_>(publisher) 
  {
    msg_.head() = {0xFE, 0xEF};
    msg_.level_flag() = 0xFF;
    msg_.gpio() = 0;

    for (auto & motor : msg_.motor_cmd())
    {
      motor.mode(0x01);
      motor.kp(0);
      motor.kd(0);
      motor.tau(0);
    }
  } 

  void Init_motor(const unitree_go::msg::dds_::LowState_& state)
  {
    // for (size_t i(0); i < msg_.motor_cmd().size(); i++) {
    for (size_t i(0); i < 12; i++) {
      msg_.motor_cmd()[i].q() = state.motor_state()[i].q();

      // Set default control gains
      msg_.motor_cmd()[i].kp(5.0);
      msg_.motor_cmd()[i].kd(1.0);
    }
  }

private:
  void TearDown() override
  {
    msg_.crc() = crc32_core((uint32_t*)&msg_, (sizeof(MsgType)>>2)-1);
  }
};

} // namespace publisher
} // namespace go2
} // namespace robot
} // namespace unitree

#endif // _UT_ROBOT_GO2_PUBLISHER_WRAPPER_H_