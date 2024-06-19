import math

class Button:
  def __init__(self) -> None:
    self.pressed = False
    self.on_pressed = False
    self.on_released = False
    self.data = 0

  def __call__(self, data) -> None:
    self.pressed = (data != 0)
    self.on_pressed = self.pressed and self.data == 0
    self.on_released = not self.pressed and self.data != 0
    self.data = data
  

class Axis:
  def __init__(self) -> None:
    self.data = 0.0
    self.pressed = False
    self.on_pressed = False
    self.on_released = False
  
    self.smooth = 0.03
    self.deadzone = 0.01
    self.threshold = 0.5

  def __call__(self, data) -> None:
    data_deadzone = 0.0 if math.fabs(data) < self.deadzone else data
    new_data = self.data * (1 - self.smooth) + data_deadzone * self.smooth
    self.pressed = math.fabs(new_data) > self.threshold
    self.on_pressed = self.pressed and math.fabs(self.data) < self.threshold
    self.on_released = not self.pressed and math.fabs(self.data) > self.threshold
    self.data = new_data


class Joystick:
  def __init__(self) -> None:
    # Buttons
    self.back = Button()
    self.start = Button()
    self.LS = Button()
    self.RS = Button()
    self.LB = Button()
    self.RB = Button()
    self.A = Button()
    self.B = Button()
    self.X = Button()
    self.Y = Button()
    self.up = Button()
    self.down = Button()
    self.left = Button()
    self.right = Button()
    self.F1 = Button()
    self.F2 = Button()

    # Axes
    self.LT = Axis()
    self.RT = Axis()
    self.lx = Axis()
    self.ly = Axis()
    self.rx = Axis()
    self.ry = Axis()
  
  def update(self):
    """
    根据原数据更新当前手柄键值
    用于on_pressed等标志位的更新

    Examples:
    >>> new_A_data = 1
    >>> self.A( new_A_data )
    """
    pass

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # Disable pygame welcome message
import pygame

class PyGameJoystick(Joystick):
  def __init__(self) -> None:
    super().__init__()

    pygame.init()
    pygame.joystick.init()
    if pygame.joystick.get_count() <= 0:
      raise Exception("No joystick found!")
    
    self._joystick = pygame.joystick.Joystick(0)
    self._joystick.init()

  def print(self):
    print("\naxes: ")
    for i in range(self._joystick.get_numaxes()):
      print(self._joystick.get_axis(i), end=" ")
    print("\nbuttons: ")
    for i in range(self._joystick.get_numbuttons()):
      print(self._joystick.get_button(i), end=" ")
    print("\nhats: ")
    for i in range(self._joystick.get_numhats()):
      print(self._joystick.get_hat(i), end=" ")
    print("\nballs: ")
    for i in range(self._joystick.get_numballs()):
      print(self._joystick.get_ball(i), end=" ")
    print("\n")

class LogicJoystick(PyGameJoystick):
  """ Logic F710 """
  def __init__(self) -> None:
    super().__init__()

  def update(self):
    pygame.event.pump()

    self.back(self._joystick.get_button(6))
    self.start(self._joystick.get_button(7))
    self.LS(self._joystick.get_button(9))
    self.RS(self._joystick.get_button(10))
    self.LB(self._joystick.get_button(4))
    self.RB(self._joystick.get_button(5))
    self.A(self._joystick.get_button(0))
    self.B(self._joystick.get_button(1))
    self.X(self._joystick.get_button(2))
    self.Y(self._joystick.get_button(3))

    self.LT((self._joystick.get_axis(2) + 1)/2)
    self.RT((self._joystick.get_axis(5) + 1)/2)
    self.rx(self._joystick.get_axis(3))
    self.ry(-self._joystick.get_axis(4))


    # 罗技手柄有2种模式
    # mode 1: light down
    self.up(1 if self._joystick.get_hat(0)[1] > 0.5 else 0)
    self.down(1 if self._joystick.get_hat(0)[1] < -0.5 else 0)
    self.left(1 if self._joystick.get_hat(0)[0] < -0.5 else 0)
    self.right(1 if self._joystick.get_hat(0)[0] > 0.5 else 0)
    self.lx(self._joystick.get_axis(0))
    self.ly(-self._joystick.get_axis(1))
    # mode 2: light up
    # self.up(1 if self._joystick.get_axis(1) < -0.5 else 0)
    # self.down(1 if self._joystick.get_axis(0) > 0.5 else 0)
    # self.left(1 if self._joystick.get_axis(0) < -0.5 else 0)
    # self.right(1 if self._joystick.get_axis(0) > 0.5 else 0)
    # self.lx(self._joystick.get_hat(0)[1])
    # self.ly(self._joystick.get_hat(0)[1])

