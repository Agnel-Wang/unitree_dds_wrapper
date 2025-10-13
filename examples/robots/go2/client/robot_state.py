from unitree_dds_wrapper.robots import go2


rs = go2.client.RobotState()
rs.timeout_s = 1.0
_ = rs.service_list()

for module in rs.service_list():
    if module["name"] == "ai_sport":
        print(module["status"])