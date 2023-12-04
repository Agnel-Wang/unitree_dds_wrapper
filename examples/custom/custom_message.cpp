#include "unitree/dds_wrapper/common/Subscription.h"
#include "unitree/dds_wrapper/common/Publisher.h"

#include "CustomMsg_.hpp"

using MessageType = unitree::msg::dds_::CustomMessage_;
const std::string TOPIC_NAME = "rt/custom_message";

namespace publisher 
{
  class CustomMessage : public unitree::robot::PublisherBase<MessageType>
  {
  public:
    CustomMessage() : PublisherBase<MessageType>(TOPIC_NAME) {}
  };

  class RealTimeCustomMessage : public unitree::robot::RealTimePublisher<MessageType>
  {
  public:
    RealTimeCustomMessage(PublisherSharedPtr publisher = std::make_shared<CustomMessage>())
    : RealTimePublisher<MessageType>(publisher)
    {
      // If you want to use vector_type message, 
      // you should initialize the vector_type message size.
      msg_.vector_data().resize(3);
    }
  };
};

namespace subscription
{
  class CustomMessage : public unitree::robot::SubscriptionBase<MessageType>
  {
  public:
    CustomMessage() : SubscriptionBase<MessageType>(TOPIC_NAME) {}
  };
};

int main(int argc, char** argv)
{
  unitree::robot::ChannelFactory::Instance()->Init(0);

  auto pub = std::make_unique<publisher::RealTimeCustomMessage>();
  auto sub = std::make_shared<subscription::CustomMessage>();

  int count = 0;
  while (true)
  {
    if(pub && pub->trylock())
    {
      pub->msg_.u8_data(count);

      pub->unlockAndPublish();
    }

    usleep(1000);
    std::cout << "Publisher: " << (int)pub->msg_.u8_data() << "\t"
              << "Subscriber: " << (int)sub->msg_.u8_data()
              << std::endl;    
    count++;
    sleep(1);
  }

  return 0;
}