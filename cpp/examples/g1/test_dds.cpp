#include "unitree/dds_wrapper/robots/g1/g1.h"

int main(int argc, char** argv)
{
    // Init DDS
    std::string iface = (argc > 1) ? argv[1] : "";
    unitree::robot::ChannelFactory::Instance()->Init(0, iface);

    auto pub = std::make_unique<unitree::robot::g1::publisher::LowState>("rt/lowstate");
    auto sub = std::make_shared<unitree::robot::g1::subscription::LowState>("rt/lowstate");

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

