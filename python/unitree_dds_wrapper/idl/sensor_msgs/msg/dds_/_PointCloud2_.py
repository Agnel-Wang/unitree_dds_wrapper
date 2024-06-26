"""
  Generated by Eclipse Cyclone DDS idlc Python Backend
  Cyclone DDS IDL version: v0.11.0
  Module: sensor_msgs.msg.dds_
  IDL file: PointCloud2_.idl

"""

from enum import auto
from typing import TYPE_CHECKING, Optional
from dataclasses import dataclass, field

import cyclonedds.idl as idl
import cyclonedds.idl.annotations as annotate
import cyclonedds.idl.types as types

# root module import for resolving types
# import sensor_msgs

# if TYPE_CHECKING:
#     import std_msgs.msg.dds_

from unitree_dds_wrapper.idl import std_msgs


@dataclass
@annotate.final
@annotate.autoid("sequential")
class PointCloud2_(idl.IdlStruct, typename="sensor_msgs.msg.dds_.PointCloud2_"):
    header: 'unitree_dds_wrapper.idl.std_msgs.msg.dds_.Header_' = field(default_factory=lambda: std_msgs.msg.dds_.Header_())
    height: types.uint32 = field(default_factory=lambda: 0)
    width: types.uint32 = field(default_factory=lambda: 0)
    fields: types.sequence['unitree_dds_wrapper.idl.sensor_msgs.msg.dds_.PointField_'] = field(default_factory=lambda: [])
    is_bigendian: bool = field(default_factory=lambda: False)
    point_step: types.uint32 = field(default_factory=lambda: 0)
    row_step: types.uint32 = field(default_factory=lambda: 0)
    data: types.sequence[types.uint8] = field(default_factory=lambda: [])
    is_dense: bool = field(default_factory=lambda: False)


