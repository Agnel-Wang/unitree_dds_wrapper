#include "unitree/dds_wrapper/go2/go2_sub.h"
#include "unitree/dds_wrapper/go2/go2_pub.h"
#include <unitree/common/thread/recurrent_thread.hpp>

/**
 * @brief Check whether the unitree high-level controller has been closed.
 * 
 * Only one program can send the lowcmd at the same time.
 */
bool check_sportmode_has_closed()
{
  auto low_cmd_sub = std::make_shared<unitree::robot::go2::subscription::LowCmd>();
  sleep(1);
  return low_cmd_sub->isTimeout();
}

int main(int argc, char** argv)
{
  // Init DDS
  std::string iface = (argc > 1) ? argv[1] : "";
  unitree::robot::ChannelFactory::Instance()->Init(0, iface);

  // Make sure the sportmode has been closed.
  if(!check_sportmode_has_closed())
  {
    std::cout << "[FATAL] SportModeController is still running" << std::endl;
    exit(1);
  }

  auto low_state = std::make_shared<unitree::robot::go2::subscription::LowState>();

  // Check the communication with the robot.  
  auto start_time = std::chrono::steady_clock::now();
  while (true)
  {
    if(!low_state->isTimeout()) {
      break;
    }

    auto now = std::chrono::steady_clock::now();
    auto elasped_time = now - start_time;
    if(elasped_time > std::chrono::seconds(3))
    {
      std::cout << "[ERROR] Cannot communicate with the robot" << std::endl;
      exit(1);
    }
  }
  
  auto low_cmd = std::make_unique<unitree::robot::go2::publisher::RealTimeLowCmd>();
  auto low_cmd_sub = std::make_shared<unitree::robot::go2::subscription::LowCmd>();

  std::cout << "WARNNING: The motor front-right leg is going to move." << std::endl
    << "Press Enter to continue..." << std::endl;
  std::cin.ignore();

  // Init the control parameters
  id_t id = 2;
  low_cmd->Init_motor(low_state->msg_); // Set gains
  double q_start = low_state->msg_.motor_state()[id].q();
  double q_mid = -2.0;

  // Control loop
  int count = 0;
  auto control_thread = std::make_shared<unitree::common::RecurrentThread>(
    2000, [&](){
      count += 1;

      if(low_cmd->trylock())
      {
        if( count < 200) {
          // Move to q_mid
          low_cmd->msg_.motor_cmd()[id].q() = q_start + (q_mid - q_start) * count / 200.;
        }
    
        low_cmd->msg_.motor_cmd()[id].q() = q_mid - 0.9 * std::sin(count / 400.);
        low_cmd->unlockAndPublish();
        std::cout << "Motor" << id << " q "
                << " cmd: "<< low_cmd_sub->msg_.motor_cmd()[id].q()
                << " state: "<< low_state->msg_.motor_state()[id].q()
                << "\r" << std::flush;
      }
    }
  );

  while (true) {
    sleep(1);
  }

  return 0;
}