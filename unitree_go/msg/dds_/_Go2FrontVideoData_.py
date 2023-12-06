"""
  Generated by Eclipse Cyclone DDS idlc Python Backend
  Cyclone DDS IDL version: v0.11.0
  Module: unitree_go.msg.dds_
  IDL file: Go2FrontVideoData_.idl

"""

from enum import auto
from typing import TYPE_CHECKING, Optional
from dataclasses import dataclass, field

import cyclonedds.idl as idl
import cyclonedds.idl.annotations as annotate
import cyclonedds.idl.types as types

# root module import for resolving types
import unitree_go


@dataclass
@annotate.final
@annotate.autoid("sequential")
class Go2FrontVideoData_(idl.IdlStruct, typename="unitree_go.msg.dds_.Go2FrontVideoData_"):
    time_frame: types.uint64 = field(default_factory=lambda: 0)
    video720p: types.sequence[types.uint8] = field(default_factory=lambda: [])
    video360p: types.sequence[types.uint8] = field(default_factory=lambda: [])
    video180p: types.sequence[types.uint8] = field(default_factory=lambda: [])


