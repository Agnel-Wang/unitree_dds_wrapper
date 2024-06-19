# Unitree_DDS_Wrapper

This project aims to simplify the communication with [Unitree Robots](https://github.com/unitreerobotics).

There is no need to implement DDS `publisher` & `subscriber` each time.

## Usage

**Dependencies**
+ [unitree_sdk2](https://github.com/unitreerobotics/unitree_sdk2)

### CPP

```bash
cd {path_to_repo}/idl/_generate_cpp
bash cxx_gen.sh
mv lib/libunitree_idl_x86_64.a {path_to_repo}/cpp/lib/{SYSTEM_PRECESSOR}/
cd {path_to_repo}/cpp
sudo ./install.sh
```

### Python

```bash
cd {path_to_repo}/python
pip install pygame # for joystick
pip install -e .
```