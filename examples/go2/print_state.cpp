#include "unitree_dds_wrapper/go2/go2_sub.h"

int main(int argc, char** argv)
{
  // Init DDS
  std::string iface = (argc > 1) ? argv[1] : "";
  unitree::robot::ChannelFactory::Instance()->Init(0, iface);

  auto low_state = std::make_shared<unitree::robot::go2::subscription::LowState>();
  auto sport_state = std::make_shared<unitree::robot::go2::subscription::SportModeState>();

  std::cout << std::fixed << std::setprecision(3) << std::endl;
  while (true)
  {
    std::cout <<" ***** Low State ***** " << std::endl;
    low_state->update();
    std::cout <<"[Joystick] lx: " << low_state->joystick.lx() << std::endl;
    std::cout <<"[Motor0 state] q: " << low_state->msg_.motor_state()[0].q() << std::endl;
    std::cout <<"[IMU] " << low_state->imu.rpy.transpose() << std::endl;

    if(!sport_state->isTimeout())
      std::cout <<" ***** SportMode State ***** " << std::endl;
      std::cout <<"mode: " << sport_state->state_name() << std::endl;
      std::cout <<"position: " << sport_state->position().transpose()
                << " velocity: " << sport_state->velocity().transpose() << std::endl;

    printf("\n\n\n\n");
    usleep(400);
  }

  return 0;
}

