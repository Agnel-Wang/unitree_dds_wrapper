

from unitree_dds_wrapper.client import Client
import json
from enum import IntEnum


API_ID_EXECUTE_UNITREE_ACTION = 7106
API_ID_GET_ACTIONS = 7107
API_ID_EXECUTE_CUSTOM_ACTION = 7108
API_ID_RENAME_CUSTOM_ACTION = 7109
API_ID_TEACH = 7110
API_ID_PAUSE_TEACH = 7111
API_ID_DELETE_TEACH_ACTION = 7112
API_ID_STOP_CUSTOM_ACTION = 7113

class ArmStatusCode(IntEnum):
    SUCCESS = 0
    COMMON = 7399
    ARMSDK_OCCUPIED = 7400
    ARM_HOLDING = 7401
    INVALID_ACTION_ID = 7402
    LOAD_ACTION_FILE = 7403
    FSM_UNAVAILABLE = 7404
    ACTION_FILE_EXIST = 7405
    LOW_BATTERY = 7406
    ERROR_MOTOR = 7407

class ArmClient(Client):
    def __init__(self):
        super().__init__('arm')

    def execute_unitree_action(self, action_id: int):
        """ 执行宇树预设动作，由ID索引，其中99为释放动作
        部分动作结束后会保持在最后一个关键帧位置; 可发送 id = 99 或 同样的id 释放

        # rt/arm/action/state
        {
            "holding": false, # 执行动作结束后是否保持在原处; 最多保持20s就会释放
            "id": 99,
            "name": "release_arm",
        }
        """
        parameter = json.dumps({"action_id": action_id})
        ret, _ = self.call(API_ID_EXECUTE_UNITREE_ACTION, parameter)
        return ret
    
    def execute_custom_action(self, action_name: str):
        """ 执行自定义示教动作; 由名称索引

        # rt/arm/action/state
        {
            "holding": false,
            "id": 100, # 一直都是100; 由name确定该动作
            "name": "a",
        }
        """
        parameter = json.dumps({"action_name": action_name})
        ret, _ = self.call(API_ID_EXECUTE_CUSTOM_ACTION, parameter)
        return ret
    
    def teach(self, action_name: str = ""):
        """ 执行示教, 记录当前上肢轨迹，腰部仅yaw支持示教。
        
        - 如若同名动作已存在，则会覆盖原有动作，且不提醒。
        - 示教最大时间限制为180s; 

        # rt/arm/action/state
        {
            "holding": false,
            "id": -1, # 示教时 由 0 变为 1, 示教介绍先变为 99 释放， 再变为 0
            "name": "",
        }
        """
        parameter = json.dumps({"action_name": action_name})
        ret, _ = self.call(API_ID_TEACH, parameter)
        return ret
    
    def teach_tick(self):
        """ 需要在示教时不断tick 否则10s后会自动退出示教。"""
        return self.teach("")

    def stop_teach(self):
        """ 停止示教
        无论如何(即使当前并未示教) 立即返回 0
        """
        ret, _ = self.call(API_ID_TEACH, "")
        return ret

    def pause_teach(self, pause: bool = True):
        """ 暂停/恢复 示教
        - pause 需显式指定是否暂停
        无论如何 立即返回 0

        # rt/arm/action/state
        id 仍为 -1
        """
        parameter = json.dumps({"pause": pause})
        ret, _ = self.call(API_ID_PAUSE_TEACH, parameter)
        return ret

    def actions(self):
        """ 获取当前所有可用动作 解析详见 __str__"""
        ret, res = self.call(API_ID_GET_ACTIONS, "")
        if ret != 0:
            print(f"Failed to get actions, error code: {ret}")
            return None
        return json.loads(res)

    def rename_custom_action(self, pre_name: str, new_name: str):
        """ 重命名自定义示教动作 """
        parameter = json.dumps({"pre_name": pre_name, "new_name": new_name})
        ret, _ = self.call(API_ID_RENAME_CUSTOM_ACTION, parameter)
        return ret

    def delete_custom_action(self, action_name: str):
        """ 删除自定义示教动作 """
        parameter = json.dumps({"action_name": action_name})
        ret, _ = self.call(API_ID_DELETE_TEACH_ACTION, parameter)
        return ret

    def stop_custom_action(self):
        """ 停止当前正在执行的自定义示教动作 """
        ret, _ = self.call(API_ID_STOP_CUSTOM_ACTION, "")
        return ret

    def __str__(self):
        msg = "G1 Arm Client\n"
        actions = self.actions()
        if actions is None:
            return "Failed to get actions."
        unitree_actions, custom_actions = actions
        msg += f"Available unitree actions: \n"
        msg += f"  - id: action name\n"
        for action in unitree_actions:
            msg += f"  - {action['id']}: {action['name']}\n"
        msg += f"Available custom actions: \n"
        for action in custom_actions:
            msg += f"  - {action['name']} : {action['time']} \n"
        return msg
    
if __name__ == "__main__":
    import sys
    import time
    import argparse
    parser = argparse.ArgumentParser(description="G1 Arm Client")
    parser.add_argument("--switch", type=int, help="Swtich service status; 0 close, 1 open")
    parser.add_argument("-i", "--id", type=int, help="Unitree action ID to execute")
    parser.add_argument("-l", "--list", action="store_true", help="List available actions")
    parser.add_argument("--name", type=str, help="Custom action Name to execute")
    parser.add_argument("--rename", type=str, nargs=2, metavar=('pre_name', 'new_name'),
                        help="Rename custom action from pre_name to new_name")
    parser.add_argument("--teach", type=str, help="Teach a new action with the given name")
    parser.add_argument("--stop_teach", action="store_true", help="Stop teaching mode if it is active")
    parser.add_argument("--pause_teach", action="store_true", help="Pause teaching mode if it is active")
    parser.add_argument("--resume_teach", action="store_true", help="Pause teaching mode if it is active")
    parser.add_argument("-d", "--delete", type=str, help="delete a custom action")
    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help()
        exit(0)
    ret = 0

    from unitree_dds_wrapper.robots.go2.client import RobotState
    robot_state = RobotState()
    if args.switch is not None:
        ret = robot_state.service_switch("g1_arm_example", args.switch)
        print(f"Service switch returned: {ret}")

    client = ArmClient()
    client.timeout_s = 10.0 # 如果是自定义的动作，是180s上限，这个10s会超时

    if args.id is not None:
        ret = client.execute_unitree_action(args.id)
    elif args.list:
        print(client)
    elif args.name is not None:
        ret = client.execute_custom_action(args.name)
    elif args.rename is not None:
        pre_name, new_name = args.rename
        ret = client.rename_custom_action(pre_name, new_name)
    elif args.teach is not None:
        ret = client.teach(args.teach)
    elif args.stop_teach:
        ret = client.stop_teach()
    elif args.pause_teach:
        ret = client.pause_teach(True)
    elif args.resume_teach:
        ret = client.pause_teach(False)
    elif args.delete is not None:
        ret = client.delete_custom_action(args.delete)
    if ret != 0:
        print(f"Action execution failed with error code: {ret}")


    if args.teach is not None:
        while True:
            ret = client.teach() # tick
            time.sleep(1)

    time.sleep(1.0)