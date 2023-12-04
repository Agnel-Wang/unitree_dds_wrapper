"""
  Generated by Eclipse Cyclone DDS idlc Python Backend
  Cyclone DDS IDL version: v0.11.0
  Module: unitree_go.msg.dds_
  IDL file: PathPoint_.idl

"""

from enum import auto
from typing import TYPE_CHECKING, Optional
from dataclasses import dataclass

import cyclonedds.idl as idl
import cyclonedds.idl.annotations as annotate
import cyclonedds.idl.types as types

# root module import for resolving types
import unitree_go


@dataclass
@annotate.final
@annotate.autoid("sequential")
class PathPoint_(idl.IdlStruct, typename="unitree_go.msg.dds_.PathPoint_"):
    t_from_start: types.float32
    x: types.float32
    y: types.float32
    yaw: types.float32
    vx: types.float32
    vy: types.float32
    vyaw: types.float32


