# 循环调度

OAS 默认使用 `next_run` 的定时调度。`script.optimization.schedule_mode` 可以切换到循环调度：

```yaml
script:
  optimization:
    schedule_mode: loop
  loop:
    enable: true
    start_task: Exploration
    probe: realm_raid_ticket
    operator: ">"
    threshold: 0
    target_task: RealmRaid
    else_task: ""
    interval: 300
    max_polls: 0
    rest_every: 0
    rest_duration: 1800
    timeout_minutes: 360
```

含义：

```
Exploration 完成
  -> 检查突破券数量
  -> 大于 0：执行 RealmRaid
  -> 不大于 0：等待 interval 后继续检查
  -> RealmRaid 完成后回到 Exploration
```

字段：

| 字段 | 说明 |
|---|---|
| `schedule_mode` | `time` 定时调度；`loop` 循环调度 |
| `start_task` | 每轮先执行的任务，大驼峰或下划线均可 |
| `probe` | `always` 或 `realm_raid_ticket` |
| `operator` / `threshold` | 探针值与阈值的比较 |
| `target_task` | 条件成立时执行的任务 |
| `else_task` | 轮询结束后的兜底任务，留空则回到起始任务 |
| `interval` | 两次探针间隔（秒） |
| `max_polls` | 每轮最多检查次数，`0` 表示不限 |
| `rest_every` | 每检查 N 次休息一次，`0` 表示不额外休息 |
| `rest_duration` | 休息时长（秒） |
| `timeout_minutes` | 一轮轮询的总超时（分钟），`0` 表示不限制 |

实现说明：

- 循环模式完全忽略任务的 `next_run` 和定时调度器。
- 探针通过隐藏任务 `tasks/LoopProbe` 执行；它复用 GameUi 导航和任务自身的 OCR 资产。
- `max_polls=0` 时会按 `interval` / `rest_every` 持续轮询，直到条件成立、`timeout_minutes` 到达或手动停止。
- 循环模式仍经过正常的 `Script.run()`，因此队列模式、防封和失败处理继续生效。
- 任务失败或客户端掉线时，任务自己排入的 `Restart` 会在循环模式下立即执行。
