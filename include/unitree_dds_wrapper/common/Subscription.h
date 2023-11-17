#ifndef _UT_ROBOT_SUBSCRIPTION_H_
#define _UT_ROBOT_SUBSCRIPTION_H_

#include <unitree/robot/channel/channel_subscriber.hpp>
#include <mutex>

namespace unitree
{
namespace robot
{

template <typename MessageType>
class SubscriptionBase
{
public:
  using MsgType = MessageType;
  
  SubscriptionBase(const std::string& topic)
  {
    last_update_time_ = std::chrono::steady_clock::now() - std::chrono::milliseconds(timeout_ms_);
    sub_ = std::make_shared<unitree::robot::ChannelSubscriber<MessageType>>(topic);
    sub_->InitChannel([this](const void *msg){
      last_update_time_ = std::chrono::steady_clock::now();
      std::lock_guard<std::mutex> lock(mutex_);
      msg_ = *(const MessageType*)msg;
    });
  }

  void set_timeout_ms(int timeout_ms)
  {
    timeout_ms_ = timeout_ms > 0 ? timeout_ms : 0;
  }

  bool isTimeout()
  {
    return std::chrono::duration_cast<std::chrono::milliseconds>(
      std::chrono::steady_clock::now() - last_update_time_).count() > timeout_ms_;
  }
  MessageType msg_;
protected:
  int timeout_ms_{1000};
  std::mutex mutex_;
  unitree::robot::ChannelSubscriberPtr<MessageType> sub_;
  std::chrono::steady_clock::time_point last_update_time_;
};


}; // namespace robot
}; // namespace unitree

#endif // _UT_ROBOT_SUBSCRIPTION_H_