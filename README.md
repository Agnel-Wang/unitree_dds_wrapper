# Unitree_DDS_Wrapper

This project aims to simplify the communication with [Unitree Robots](https://github.com/unitreerobotics).

There is no need for each one to implement DDS `publisher` & `subscriber` every time.


## Setup

**Dependencies**
+ [unitree_sdk2](https://github.com/unitreerobotics/unitree_sdk2)

```
sudo cp -r include/unitree_dds_wrapper /usr/local/include/unitree
```

## Examples

+ **Subscriber**

```cpp
auto low_state = std::make_shared<unitree::robot::go2::subscription::LowState>();

while(true)
{
  low_state->update();
  std::cout <<"[Joystick] lx: " << low_state->joystick.lx() << std::endl;
  std::cout <<"[Motor0 state] q: " << low_state->msg_.motor_state()[0].q() << std::endl;
  std::cout <<"[IMU] " << low_state->imu.rpy.transpose() << std::endl;

  sleep(1);
}
```

+ **Publisher**

```cpp
auto low_cmd = std::make_unique<unitree::robot::go2::publisher::RealTimeLowCmd>();
auto low_state = std::make_shared<unitree::robot::go2::subscription::LowState>();

low_cmd->Init_motor(low_state->msg_); // set default gains

double q_mid = -2.0;
int count = 0;
while(true)
{
  if(low_cmd->trylock())
  {
    low_cmd->msg_.motor_cmd()[2].q() = q_mid + 0.9 * std::sin(count / 400.);

    low_cmd->unlockAndPublish();
  }

  count += 1;
  usleep(2000);
}
```

## Custom message

You can also add your custom message easily.

1. Define your idl message. (see [CustomMsg_.idl](idl/CustomMsg_.idl))
2. Generate cpp file
```bash
cd idl
./cxx_gen.sh
```
This will generate `include`&`lib` directories in idl directory.
3. See example [custom_message.cpp](examples/custom/custom_message.cpp)
```
cd build
cmake -DBUILD_CUSTOM_MESSAGE=True ..
make
./custom_message
```
