#ifndef _UT_ROBOT_GO2_SUBSCRIPTION_WRAPPER_H_
#define _UT_ROBOT_GO2_SUBSCRIPTION_WRAPPER_H_

#include <eigen3/Eigen/Dense>
#include <unordered_map>
#include "unitree_dds_wrapper/common/Subscription.h"
#include "unitree_dds_wrapper/common/unitree_joystick.hpp"

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

namespace subscription
{

class LowState : public SubscriptionBase<unitree_go::msg::dds_::LowState_>
{
public:
  using SharedPtr = std::shared_ptr<LowState>;

  LowState() : SubscriptionBase<MsgType>("rt/lowstate") {}

  void update()
  {
    std::lock_guard<std::mutex> lock(mutex_);

    // ********** Joystick ********** //
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
    
    // ********** IMUState ********** //
    auto imu_state = msg_.imu_state();
    imu.quaternion = Eigen::Map<Eigen::Quaternionf>(msg_.imu_state().quaternion().data());
    imu.gyroscope = Eigen::Map<const Eigen::Vector3f>(imu_state.gyroscope().data());
    imu.accelerometer = Eigen::Map<const Eigen::Vector3f>(imu_state.accelerometer().data());
    imu.rpy = Eigen::Map<const Eigen::Vector3f>(imu_state.rpy().data());
    imu.temperature = imu_state.temperature();
  }

  unitree::common::UnitreeJoystick joystick;

  struct IMUState{
    Eigen::Quaternionf quaternion;
    Eigen::Vector3f gyroscope;
    Eigen::Vector3f accelerometer;
    Eigen::Vector3f rpy;
    int8_t temperature;
  } imu;
};

class LowCmd : public SubscriptionBase<unitree_go::msg::dds_::LowCmd_>
{
public:
  using SharedPtr = std::shared_ptr<LowCmd>;

  LowCmd() : SubscriptionBase<MsgType>("rt/lowcmd") {}
};

class SportModeState : public SubscriptionBase<unitree_go::msg::dds_::SportModeState_>
{
public:
  using SharedPtr = std::shared_ptr<SportModeState>;

  SportModeState() : SubscriptionBase<MsgType>("rt/sportmodestate") {}

  std::string state_name() const { return FSMModeStringMap.at(msg_.mode()); }

  /**
   * 0 : idle
   * 1 : trot
   * 2 : run
   * 3 : climb_stair
   * 4 : forwardDownStair
   * 9 : adjust
   */
  uint32_t    gaitType()   const { return msg_.gait_type(); }
  
  const Eigen::Vector3f position() const {
    return Eigen::Map<const Eigen::Vector3f>(msg_.position().data());
  }
  const Eigen::Vector3f velocity() const{
    return Eigen::Map<const Eigen::Vector3f>(msg_.velocity().data());
  }


private:
  const std::unordered_map<uint8_t, std::string> FSMModeStringMap = {
    {0, "idle"},
    {1, "balanceStand"},
    {2, "pose"},
    {3, "locomotion"},
    {4, "reserve"},
    {5, "lieDown"},
    {6, "jointLock"},
    {7, "damping"},
    {8, "recoveryStand"},
    {9, "reserve"},
    {10, "sit"},
    {11, "frontFlip"},
    {12, "frontJump"},
    {13, "frontPounce"},
  };
};

class LidarState : public SubscriptionBase<unitree_go::msg::dds_::LidarState_>
{
public:
  using SharedPtr = std::shared_ptr<LidarState>;

  LidarState() : SubscriptionBase<MsgType>("rt/utlidar/lidar_state") {}
};

class LidarCloud : public SubscriptionBase<sensor_msgs::msg::dds_::PointCloud2_>
{
public:
  using SharedPtr = std::shared_ptr<LidarCloud>;

  LidarCloud() : SubscriptionBase<MsgType>("rt/utlidar/cloud") {}
};

class UwbState : public SubscriptionBase<unitree_go::msg::dds_::UwbState_>
{
public:
  using SharedPtr = std::shared_ptr<UwbState>;

  UwbState() : SubscriptionBase<MsgType>("rt/uwbstate") {}
};

//TODO: other states

} // namespace subscriber
} // namespace go2
} // namespace robot
} // namespace unitree



#endif // _UT_ROBOT_GO2_SUBSCRIPTION_WRAPPER_H_