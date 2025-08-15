from enum import auto
from typing import TYPE_CHECKING, Optional
from dataclasses import dataclass, field

import cyclonedds.idl as idl
import cyclonedds.idl.annotations as annotate
import cyclonedds.idl.types as types

# root module import for resolving types

@dataclass
@annotate.final
@annotate.autoid("sequential")
class SportModeState_(idl.IdlStruct, typename="unitree_hg.msg.dds_.SportModeState_"):
    fsm_id: types.uint32 = field(default_factory=lambda: 0)
    fsm_mode: types.uint32 = field(default_factory=lambda: 0)
    task_id: types.uint32 = field(default_factory=lambda: 0)
    task_time: types.float32 = field(default_factory=lambda: 0.0)