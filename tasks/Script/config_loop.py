# This Python file uses the following encoding: utf-8
"""Loop scheduling configuration.

Loop mode runs:

    start_task -> probe condition -> target_task -> start_task -> ...

It is intentionally separate from the time-based scheduler. When
``optimization.schedule_mode == loop`` the ``next_run`` fields are ignored.
"""
from enum import Enum

from pydantic import BaseModel, Field


class LoopProbe(str, Enum):
    ALWAYS = 'always'
    REALM_RAID_TICKET = 'realm_raid_ticket'


class LoopCompare(str, Enum):
    GT = '>'
    GE = '>='
    LT = '<'
    LE = '<='
    EQ = '=='
    NE = '!='


class Loop(BaseModel):
    # 总开关；循环模式下还需要 optimization.schedule_mode = loop
    enable: bool = Field(default=False, description='loop_enable_help')
    # 每轮先执行的任务（大驼峰，如 Exploration）
    start_task: str = Field(default='Exploration', description='loop_start_task_help')
    # 任务完成后读取的探针
    probe: LoopProbe = Field(default=LoopProbe.REALM_RAID_TICKET, description='loop_probe_help')
    # 比较方式与阈值
    operator: LoopCompare = Field(default=LoopCompare.GT, description='loop_operator_help')
    threshold: int = Field(default=0, description='loop_threshold_help')
    # 条件成立时执行的任务
    target_task: str = Field(default='RealmRaid', description='loop_target_task_help')
    # 条件一直不成立时执行的任务；留空则继续轮询/回到 start_task
    else_task: str = Field(default='', description='loop_else_task_help')
    # 每轮探针间隔（秒）
    interval: int = Field(default=300, ge=5, description='loop_interval_help')
    # 每轮最多检查次数；0 = 不限次数
    max_polls: int = Field(default=0, ge=0, description='loop_max_polls_help')
    # 每检查 N 次休息一次；0 = 不额外休息
    rest_every: int = Field(default=0, ge=0, description='loop_rest_every_help')
    # 休息时长（秒）
    rest_duration: int = Field(default=1800, ge=10, description='loop_rest_duration_help')
    # 一轮轮询的总超时（分钟）；0 = 不限制
    timeout_minutes: int = Field(default=360, ge=0, description='loop_timeout_help')
