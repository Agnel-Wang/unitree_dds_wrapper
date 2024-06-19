#include "unitree/dds_wrapper/go2/go2_sub.h"
#include "unitree/dds_wrapper/go2/go2_pub.h"

int main(int argc, char** argv)
{
    // Init DDS
    std::string iface = (argc > 1) ? argv[1] : "";
    unitree::robot::ChannelFactory::Instance()->Init(0, iface);

    auto pub = std::make_unique<unitree::robot::go2::publisher::LowState>();
    auto sub = std::make_shared<unitree::robot::go2::subscription::LowState>();

    while (true)
    {
        pub->msg_.crc() = pub->msg_.crc() + 1;
        pub->unlockAndPublish();

        sleep(1);

        std::cout << "pub->msg_.crc(): " << pub->msg_.crc() << std::endl;
        std::cout << "sub->msg_.crc(): " << sub->msg_.crc() << std::endl;
    }

    return 0;
}

