from . import go2_pub as pub
from . import go2_sub as sub

from enum import IntEnum

class JointIndex(IntEnum):
    FR_Hip = 0,
    FR_Thigh = 1,
    FR_Calf = 2,
    FL_Hip = 3,
    FL_Thigh = 4,
    FL_Calf = 5,
    RR_Hip = 6,
    RR_Thigh = 7,
    RR_Calf = 8,
    RL_Hip = 9,
    RL_Thigh = 10,
    RL_Calf = 11,