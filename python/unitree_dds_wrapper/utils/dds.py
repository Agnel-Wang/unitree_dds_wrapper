import os

def set_dds_network(address = "192.168.123"):
    """查找当前设备上的网卡，获取其中以特定网段开头的网卡
    ; address IPv4的前三位
    """
    for i in os.listdir('/sys/class/net'):
        # en: 以太网
        # eth: 以太网 Centos 6 以前系统
        # wl: 无线网
        if i.startswith('en') or i.startswith('eth') or i.startswith('wl'):
            for j in os.popen('ip addr show ' + i).readlines():
                if 'inet ' in j and address in j:
                    CYCLONEDDS_URI = f"<CycloneDDS><Domain><General><NetworkInterfaceAddress>{i}</NetworkInterfaceAddress></General></Domain></CycloneDDS>"
                    os.environ["CYCLONEDDS_URI"] = CYCLONEDDS_URI
                    return