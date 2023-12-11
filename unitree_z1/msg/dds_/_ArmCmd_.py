"""
  Generated by Eclipse Cyclone DDS idlc Python Backend
  Cyclone DDS IDL version: v0.11.0
  Module: unitree_z1.msg.dds_
  IDL file: ArmCmd_.idl

"""

from enum import auto
from typing import TYPE_CHECKING, Optional
from dataclasses import dataclass, field

import cyclonedds.idl as idl
import cyclonedds.idl.annotations as annotate
import cyclonedds.idl.types as types

# root module import for resolving types
import unitree_z1


@dataclass
@annotate.final
@annotate.autoid("sequential")
class ArmCmd_(idl.IdlStruct, typename="unitree_z1.msg.dds_.ArmCmd_"):
    mode: types.uint8 = field(default_factory=lambda: 0)
    kp: types.array[types.float64, 6] = field(default_factory=lambda: [0.0] * 6)
    kd: types.array[types.float64, 6] = field(default_factory=lambda: [0.0] * 6)
    q: types.array[types.float64, 6] = field(default_factory=lambda: [0.0] * 6)
    dq: types.array[types.float64, 6] = field(default_factory=lambda: [0.0] * 6)
    tau: types.array[types.float64, 6] = field(default_factory=lambda: [0.0] * 6)
    twist: 'unitree_z1.msg.dds_.Twist_' = field(default_factory=lambda: unitree_z1.msg.dds_.Twist_())
    pose: 'unitree_z1.msg.dds_.Pose_' = field(default_factory=lambda: unitree_z1.msg.dds_.Pose_())
    gripper: 'unitree_z1.msg.dds_.GripperCommand_' = field(default_factory=lambda: unitree_z1.msg.dds_.GripperCommand_())


