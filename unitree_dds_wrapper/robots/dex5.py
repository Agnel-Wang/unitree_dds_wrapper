from unitree_dds_wrapper.publisher import Publisher
from unitree_dds_wrapper.subscription import Subscription
from unitree_dds_wrapper.idl import unitree_hg
import numpy as np

NUM_MOTORS = 16
NUM_JOINTS = 20

DEFAULT_KP = np.array(
    [
        10.0, 5.0, 5.0, 5.0,
        0.02, 0.02, 0.02, 
        0.02, 0.02, 0.02, 
        0.02, 0.02, 0.02,  
        0.02, 0.02, 0.02, 
    ],
    dtype=np.float64,
)

JOINT2URDF_INDEX = [
    4, 5, 6, 6,  # index
    7, 8, 9, 9,  # middle
    10, 11, 12, 12,  # ring
    13, 14, 15, 15,  # little
    0, 1, 2, 3      # thumb
]

JOINT_INDEX = [
    4, 5, 6, 7, 
    8, 9, 10, 11,
    12, 13, 14, 15,
    16, 17, 18, 19,  
    0, 1, 2, 3,   # thumb
]

DEFAULT_KD = np.array(
    [
        0.9, 0.4, 0.4, 0.4,
        0.0004, 0.0004, 0.0004, 
        0.0004, 0.0004, 0.0004, 
        0.0004, 0.0004, 0.0004, 
        0.0004, 0.0004, 0.0004, 
    ],
    dtype=np.float64,
)

# type: left or right
class Dex5CmdPublisher(Publisher):
    def __init__(self, type: str, participant = None):
        if type not in ["left", "right"]:
            raise Exception
        super().__init__(unitree_hg.msg.dds_.HandCmd_, f"rt/dex5/{type}/cmd", participant)
        self.msg: unitree_hg.msg.dds_.HandCmd_

# type: left or right
class Dex5StateSubscriber(Subscription):
    def __init__(self, type: str, participant = None):
        super().__init__(unitree_hg.msg.dds_.HandState_, f"rt/dex5/{type}/state", participant)
        self.msg: unitree_hg.msg.dds_.HandState_

        self.q = np.zeros(NUM_JOINTS)
        self.dq = np.zeros(NUM_JOINTS)
        self.tau = np.zeros(NUM_JOINTS)
        self.temperature = np.zeros(NUM_JOINTS)


    def post_communication(self):
        for idx, j_id in enumerate(JOINT_INDEX):
            m = self.msg.motor_state[idx]
            self.q[j_id] = m.q
            self.dq[j_id] = m.dq
            self.tau[j_id] = m.tau_est
            self.temperature[j_id] = m.temperature[0]