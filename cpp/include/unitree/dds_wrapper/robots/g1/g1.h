#pragma once

#include <unitree/dds_wrapper/robots/g1/g1_pub.h>
#include <unitree/dds_wrapper/robots/g1/g1_sub.h>

namespace unitree
{
namespace robot
{
namespace g1
{

/**
 * @brief Check the hand type.
 * 
 * @return HandType 
 */
inline HandType check_hand_type()
{   
    auto inspire = std::make_shared<g1::subscription::InspireHandState>();
    auto dex3_left = std::make_shared<g1::subscription::Dex3LeftHandState>();
    std::this_thread::sleep_for(std::chrono::milliseconds(300));

    if(!inspire->isTimeout()) return HandType::Inspire;
    if(!dex3_left->isTimeout()) return HandType::Dex3;
    return HandType::None;
}

} // namespace g1
} // namespace robot
} // namespace unitree