#ifndef _UT_COMMON_JOYSTICK_HPP_
#define _UT_COMMON_JOYSTICK_HPP_

#include <math.h>
#include <stdint.h>

namespace unitree
{
namespace common
{
    
// ***************************** Unitree Joystick Data Type ***************************** //

typedef union
{
  struct
  {
    uint8_t R1 : 1;
    uint8_t L1 : 1;
    uint8_t Start : 1;
    uint8_t Select : 1;
    uint8_t R2 : 1;
    uint8_t L2 : 1;
    uint8_t f1 : 1;
    uint8_t f2 : 1;
    uint8_t A : 1;
    uint8_t B : 1;
    uint8_t X : 1;
    uint8_t Y : 1;
    uint8_t up : 1;
    uint8_t right : 1;
    uint8_t down : 1;
    uint8_t left : 1;
  } components;

  uint16_t value;
} BtnUnion;

typedef struct
{
  uint8_t head[2];
  BtnUnion btn;
  float lx;
  float rx;
  float ry;
  float L2;
  float ly;
} BtnDataStruct;         

typedef union
{
  BtnDataStruct RF_RX;
  uint8_t buff[40];   //凑40字节
}REMOTE_DATA_RX;

// ***************************** Button & Axis ***************************** //

template <typename T> // int, bool, string
class Button
{
public:
  void operator()(const T& data){ // update
    pressed = (data != dataNull_);
    on_pressed = (pressed && data_ == dataNull_);
    on_released = (!pressed && data_ != dataNull_);
    data_ = data;
  }
  const T& operator()() { return data_; }

  bool pressed = false;
  bool on_pressed = false;
  bool on_released = false;
private:
  T data_{}, dataNull_{};
};

class Axis
{
public:
  void operator()(const float& data){ // update
    auto data_deadzone = std::fabs(data) < deadzone ? 0.0 : data;
    double new_data = data_ * (1.0 - smooth) + data_deadzone * smooth;
    pressed = (new_data > threshold);
    on_pressed = (pressed && data_ < threshold);
    on_released = (!pressed && data_ > threshold);
    data_ = new_data;
  }

  const float& operator()() { return data_; }

  float smooth = 0.03;
  float deadzone = 0.01;

  // Change an axis value to a button
  bool pressed = false;
  bool on_pressed = false;
  bool on_released = false;
  float threshold{0.5};
private:
  float data_{};
};

// ***************************** Unitree Joystick Interface ***************************** //

struct UnitreeJoystick
{
  // 采用标准手柄键位名称
  Button<int> back;
  Button<int> start;
  // Button<int> LS;
  // Button<int> RS;
  Button<int> LB;
  Button<int> RB;
  Button<int> A;
  Button<int> B;
  Button<int> X;
  Button<int> Y;
  Button<int> up;
  Button<int> down;
  Button<int> left;
  Button<int> right;
  Button<int> F1;
  Button<int> F2;
  Axis lx;
  Axis ly;
  Axis rx;
  Axis ry;
  Axis LT;
  Axis RT;
};

} // namespace common
} // namespace unitree

#endif//_UT_COMMON_JOYSTICK_HPP_

