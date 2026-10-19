---
name: coros-training
display_name: 高驰训练
display_name_en: COROS Training
description: 当用户提到高驰、COROS、跑步、骑行、越野、运动记录、配速、心率、睡眠、HRV、压力、恢复、跑力、VO2max、训练负荷、训练计划、课程或日程时使用。覆盖官方 COROS MCP 的全部工具：读取运动、睡眠、恢复与体能数据，并在用户明确要求保存、创建、修改或排期时写入训练计划、课程库模板和每日排期。
description_zh: 查询高驰运动、睡眠、恢复和体能，并在用户确认后创建、修改或排期训练计划与课程。
description_en: Review COROS activities, sleep, recovery and fitness, and create, update or schedule training plans, library workouts and daily sessions after the user asks to save.
version: 1.0.0
author: COROS Connector
---

# 高驰 COROS

通过已安装的高驰训练连接器调用官方 MCP。工具名称、参数和返回字段以当前连接刷新后的工具定义为准。本技能只说明路由和安全边界；不要根据记忆猜测未出现在工具定义里的字段。

工具清单见 @references/tools.md。

## 开始之前

1. 确认「高驰训练」连接器已连接。用户可能同时装有市场的官方「高驰」连接器，那个版本只支持读取；本技能涉及的创建和修改工具在官方版上不存在。未连接、401、invalid_token 或授权失效时，停止调用，请用户在 WorkBuddy 里重新连接「高驰训练」，不要要求用户把 Token 粘贴到对话中。工具在刷新后仍不出现，说明当前连接没有这项能力，不要用只读工具模拟写入。
2. 设备数据必须先同步到 COROS App 再上传云端。App 里没有的记录，MCP 也读不到。
3. 只读取完成当前问题所需的数据。生理周期、身高体重等个人资料仅在用户主动询问或计算确实需要时读取。
4. 内部 ID 只用于后续工具参数，用完整十进制字符串传递，不要展示给用户，也不要把计划 ID、课程库 ID 和日程副本 ID 混用。

## 先选对工具

按用户意图选择，不要为了“看起来更全”连续调用无关工具。

| 用户意图 | 调用顺序 |
| --- | --- |
| 最近运动、跑步量、配速、某次活动 | `querySportRecords`，需要细节再 `getActivityDetail`；要教练式解读再用 `analyzeActivityDetail` |
| 分圈、最后几分钟、某一段 | 先拿到活动标识，默认圈用 `queryActivityLapData`，自定义时间窗用 `queryCustomActivityLapData` |
| 原始 FIT | 优先 `downloadActivityFitFiles`；平台收不到二进制文件时再用 `queryActivityFitFileDownloadUrls` |
| 今天或近期健康概览 | `queryDailyHealthData` |
| 只问平均心率、静息心率、压力、睡眠、睡眠 HRV、恢复 | 用对应专项工具，不要用每日总览代替 |
| 跑力、VO2max、阈值配速、成绩预测 | `queryFitnessAssessmentOverview` |
| 训练负荷、是否练多了 | `queryTrainingLoadAssessment` |
| 本周或某几天练什么 | `queryTrainingSchedule` |
| 手表和账号资料 | `queryDevices`、`queryUserInfo` |

心率曲线、压力原始点和健康快测有查询窗口限制，以工具定义为准。近期天数模式通常最多 7 天；压力原始曲线最多 7 天。

FIT 文件本体和下载链接共用每个连接用户每 24 小时 50 个文件的额度。不要为了浏览而批量下载；只有用户需要原始数据时才取文件。

## 写入前必须区分保存位置

创建、修改、排期都会写入用户的高驰账号。用户只要建议、草稿或“帮我看看怎么练”时，只给出方案，不调用写入工具。用户明确说保存、创建、安排、修改、缩短或替换时，先用一句话复述将保存的内容和日期，再调用。

| 用户要的结果 | 正确路径 | 不要做成 |
| --- | --- | --- |
| 一份多周计划 | 先 `queryTrainingPlanLibrary`，确认没有未处理的重叠进行中计划后 `createTrainingPlan` | 把每周拆成一堆单独日程 |
| 修改进行中的计划 | `queryTrainingPlanLibrary` → `queryTrainingPlanDetails` → `updateTrainingPlan` | 另建一节课冒充修改 |
| 可复用课程模板 | `createSingleWorkout`；修改前先 `queryWorkoutDetails`，再 `updateWorkoutDetails` | 修改模板时期望日程副本跟着变 |
| 某一天的新课 | `createScheduledWorkout` | 先建模板再排期，除非用户明确要求两者都要 |
| 把已有课程排到某天 | `queryWorkoutLibrary` → `scheduleWorkout` | 重建一份内容相同的新课 |
| 修改某天已有的课 | `queryTrainingSchedule` 后判断归属 | 不读详情就覆盖 |

判断规则：

- 计划内课程走可编辑的执行计划。只修改 `recordRole=execution` 且 `editable=true` 的记录。
- 独立排期课程使用返回的日期和 `idInPlan`，经 `queryScheduledWorkoutDetails` 后调用 `updateScheduledWorkout`。
- 新计划覆盖 4 到 16 个自然周，开始日在今天到今天之后 14 天内。与进行中的计划重叠时，先说明重叠并得到用户确认。
- 直接排期和新建日程课程的日期范围是今天到今天之后 90 天，含两端，时区以高驰账号为准。
- 新建结构化课程只支持跑步、骑行、越野跑。课程运动类型用 1、2、5，计划休息日用 4。这些不是运动记录里的 100、200 一类编码。
- 课程库里已有的力量、游泳等课程可以排期，不能在这里新建或编辑。
- `updateTrainingPlan` 按天替换：提交的日期会替换这一天的全部课程，未提交的日期保持不变。某一天要保留的课程必须全部带上。休息条目会清空当天。已有完成课程的日期会被跳过，必须如实告诉用户。
- 修改课程库模板不影响已经排到日程上的副本。修改独立日程副本也不改变库里的原件。更新日程后，后续修改使用本次返回的 `idInPlan`。
- 改期、删除独立日程课程，以及退出或删除训练计划，仍需用户在 COROS App 中操作。不要用新建或清空所有日期来模拟这些操作，也不要绕过 `editable=false`。

编辑已有课程时，先读取完整内容，只改用户要求的部分，再提交完整课程。保留未提及的分段、强度、自由模式目标和空强度字段。

## 写完要核对

- 查看返回里的 `isError`、拒绝原因、被跳过的日期和实际保存结果。进程没报错不等于保存成功。
- 写入超时、连接中断或响应不完整时，不要立刻重试。先查询对应的计划、课程库或那一天；仍无法确认时，请用户在 COROS App 查看，确认没有重复后再决定是否重试。
- 同一天已有其他课程时告诉用户。把同一个库课程排到同一天不会再复制一份；直接新建没有同样的去重保证。
- 工具在刷新后仍不存在时，说明当前连接没有这项能力，不要声称已经保存。

## 常见异常

- 超时：连接器超时是 30 秒。查询超时可以原样重试一次。写入超时、连接中断或响应不完整时不要立刻重试，先查询对应计划、课程库或当天日程。
- 授权失效：返回未连接、401、`invalid_token` 或 `invalid_grant` 时停止调用，请用户在 WorkBuddy 重新连接「高驰训练」。不要向用户索要 Token、密码或授权码。
- 参数错误：返回参数无效、日期超出范围、运动类型不匹配或缺少必填项时，只按工具定义和上一次查询结果修正参数。缺的是用户才能决定的信息时，只询问那一项。不要编造字段来重试。
- 没有数据：先确认记录已经出现在 COROS App 云端，再缩小日期或运动类型重新查询。

## 回答

用用户的语言概括结果，带上时间范围和关键数字。配速、距离、心率、睡眠时长和恢复状态与工具返回保持一致，缺少数据就说明缺少，不要补造。需要对比趋势时先取齐同一口径的数据再下结论。
