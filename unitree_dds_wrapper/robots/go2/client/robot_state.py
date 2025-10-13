from unitree_dds_wrapper.client import Client
import json

class RobotState(Client):
    def __init__(self):
        super().__init__('robot_state')

    def service_list(self) -> list:
        ret, data = self.call(1003, "")
        return json.loads(data)
