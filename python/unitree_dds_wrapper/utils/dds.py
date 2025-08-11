import os
import re

def get_ip(address = "192.168.123."):
    """获取以特定网段开头的网卡 及其 IP地址

    Parameter
    ---------
    address: str
        IP地址的前三位 末尾加. 

    Return
    ---------
    net_dev: str
        网卡名称
    ip: str
        IP地址
    """
    for net_dev in os.listdir('/sys/class/net'):
        if net_dev.startswith('en') or net_dev.startswith('eth') or net_dev.startswith('wl'):
            for j in os.popen(f'ip addr show {net_dev} | grep -B 1 \'valid_lft forever\'  ').readlines():
                if address in j:
                    # 获取下一行
                    ip_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', j)
                    if ip_match:
                        return net_dev, ip_match.group(0)
    return None, None

def set_dds_network(address = "192.168.123"):
    """Set the DDS network interface address
    """
    net_dev, ip = get_ip(address)
    if net_dev:
        CYCLONEDDS_URI = f"<CycloneDDS><Domain><General><NetworkInterfaceAddress>{net_dev}</NetworkInterfaceAddress></General></Domain></CycloneDDS>"
        os.environ["CYCLONEDDS_URI"] = CYCLONEDDS_URI