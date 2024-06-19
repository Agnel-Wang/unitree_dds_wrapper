"""
  Generated by Eclipse Cyclone DDS idlc Python Backend
  Cyclone DDS IDL version: v0.11.0
  Module: unitree_go.msg.dds_
  IDL file: SportModeCmd_.idl

"""

from enum import auto
from typing import TYPE_CHECKING, Optional
from dataclasses import dataclass, field

import cyclonedds.idl as idl
import cyclonedds.idl.annotations as annotate
import cyclonedds.idl.types as types

# root module import for resolving types
from unitree_dds_wrapper.idl  import unitree_go


@dataclass
@annotate.final
@annotate.autoid("sequential")
class SportModeCmd_(idl.IdlStruct, typename="unitree_go.msg.dds_.SportModeCmd_"):
    mode: types.uint8 = field(default_factory=lambda: 0)
    gait_type: types.uint8 = field(default_factory=lambda: 0)
    speed_level: types.uint8 = field(default_factory=lambda: 0)
    foot_raise_height: types.float32 = field(default_factory=lambda: 0.0)
    body_height: types.float32 = field(default_factory=lambda: 0.0)
    position: types.array[types.float32, 2] = field(default_factory=lambda: [0.0, 0.0])
    euler: types.array[types.float32, 3] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    velocity: types.array[types.float32, 2] = field(default_factory=lambda: [0.0, 0.0])
    yaw_speed: types.float32 = field(default_factory=lambda: 0.0)
    bms_cmd: 'unitree_dds_wrapper.idl.unitree_go.msg.dds_.BmsCmd_' = field(default_factory=lambda: unitree_go.msg.dds_.BmsCmd_())
    path_point: types.array['unitree_dds_wrapper.idl.unitree_go.msg.dds_.PathPoint_', 30] = field(default_factory=lambda: [unitree_go.msg.dds_.PathPoint_() for _ in range(30)])

