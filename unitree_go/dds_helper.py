from unitree_go.msg import dds_

def get_imu_state():
    return dds_.IMUState_(
        quaternion=[1, 0, 0, 0],
        rpy=[0, 0, 0],
        accelerometer=[0, 0, 0],
        gyroscope=[0, 0, 0],
        temperature=0
    )


def get_bms_state():
    return dds_.BmsState_(
        version_high=0,
        version_low=0,
        status=0,
        soc=0,
        current=0,
        cycle=0,
        bq_ntc=[0, 0],
        mcu_ntc=[0, 0],
        cell_vol=[0 for _ in range(15)]
    )


def get_motor_state():
    return dds_.MotorState_(
        mode=1,
        q=0.,
        dq=0.,
        ddq=0.,
        tau_est=0.,
        q_raw=0.,
        dq_raw=0.,
        ddq_raw=0.,
        temperature=0,
        lost=0,
        reserve=[0, 0]
    )


def get_low_state():
    return dds_.LowState_(
        head=(0, 0),
        level_flag=0,
        frame_reserve=0,
        sn=(0, 0),
        version=(0, 0),
        bandwidth=0,
        imu_state=get_imu_state(),
        motor_state=[get_motor_state() for _ in range(20)],
        bms_state=get_bms_state(),
        foot_force=(0, 0, 0, 0),
        foot_force_est=(0, 0, 0, 0),
        tick=0,
        wireless_remote=[0 for _ in range(40)],
        bit_flag=0,
        adc_reel=0.,
        temperature_ntc1=0,
        temperature_ntc2=0,
        power_v=0.,
        power_a=0.,
        fan_frequency=(0, 0, 0, 0),
        reserve=0,
        crc=0
    )

def get_low_cmd():
    return dds_.LowCmd_(
        level_flag=0,
        frame_reserve=0,
        sn=(0, 0),
        version=(0, 0),
        bandwidth=0,
        imu_cmd=get_imu_state(),
        motor_cmd=[get_motor_state() for _ in range(20)],
        bms_cmd=get_bms_state(),
        foot_force=(0, 0, 0, 0),
        tick=0,
        wireless_remote=[0 for _ in range(40)],
        bit_flag=0,
        adc_reel=0.,
        temperature_ntc1=0,
        temperature_ntc2=0,
        power_v=0.,
        power_a=0.,
        fan_frequency=(0, 0, 0, 0),
        reserve=0,
        crc=0
    )
    