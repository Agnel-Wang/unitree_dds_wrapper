from unitree_dds_wrapper.robots import g1
import time
from unitree_dds_wrapper.client import ResponseSubscriber

# pub = g1.pub.LowCmd(topic="rt/test")
# sub = g1.sub.LowCmd(topic="rt/test")
# sub = g1.sub.LowCmd()
lowstate = g1.sub.LowState(autospin=False)
# lowstate.start()
# response_sub = ResponseSubscriber(topic="rt/api/test/response")

while True:
    # pub.write()
    t0 = time.time()
    lowstate.take_one()
    print(f"take_one cost: {time.time() - t0:.3f} s")
    print(time.time())
    if lowstate.msg:
        print(lowstate.msg.tick)
    print(lowstate.isTimeout())
    time.sleep(0.5)
    