from unitree_dds_wrapper.robots import h1
import numpy as np
np.set_printoptions(precision=3, suppress=True)
import time

hand = h1.pub.InspireHand()

for _ in range(5):
    time.sleep(0.5)
    hand.lq = np.zeros(6)
    hand.rq = np.ones(6)
    hand.write()

    time.sleep(0.5)
    hand.lq = np.ones(6)
    hand.rq = np.zeros(6)
    hand.write()