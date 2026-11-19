from module.base.loop import compare_value, wait_after_poll
from tasks.Script.config import Script
from tasks.Script.config_loop import Loop, LoopCompare
from tasks.Script.config_optimization import Optimization, ScheduleMode


def test_compare_value_supports_all_operators():
    assert compare_value(5, LoopCompare.GT, 0) is True
    assert compare_value(0, LoopCompare.GT, 0) is False
    assert compare_value(0, LoopCompare.GE, 0) is True
    assert compare_value(1, LoopCompare.LT, 2) is True
    assert compare_value(2, LoopCompare.LE, 2) is True
    assert compare_value(2, LoopCompare.EQ, 2) is True
    assert compare_value(2, LoopCompare.NE, 2) is False
    assert compare_value(2, ">", 1) is True


def test_loop_rest_after_n_polls():
    assert wait_after_poll(1, 300, 6, 1800) == 300
    assert wait_after_poll(5, 300, 6, 1800) == 300
    assert wait_after_poll(6, 300, 6, 1800) == 1800
    assert wait_after_poll(6, 300, 0, 1800) == 300


def test_loop_defaults_and_mode_are_separate():
    optimization = Optimization()
    assert optimization.schedule_mode == ScheduleMode.TIME

    loop = Loop()
    assert loop.enable is False
    assert loop.start_task == "Exploration"
    assert loop.target_task == "RealmRaid"
    assert loop.max_polls == 0

    script = Script()
    assert script.loop.enable is False
