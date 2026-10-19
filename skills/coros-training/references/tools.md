# 高驰 MCP 工具

以下为官方 COROS MCP 已公开的工具分组。服务器升级后以连接里刷新到的工具定义为准；这里没有列出的新工具，先读它的描述和参数再调用。

## 运动记录

| 工具 | 用途 |
| --- | --- |
| `querySportRecords` | 按日期、运动类型、距离、时长、配速、地点筛选活动，返回后续查询所需的活动标识和时间 |
| `getActivityDetail` | 读取单次活动的心率、配速或速度、海拔、步频等详情 |
| `analyzeActivityDetail` | 基于活动详情生成教练式分析，可关注配速、速度或心率 |
| `queryActivityLapData` | 读取 App 默认分圈或分段 |
| `queryCustomActivityLapData` | 读取活动内一段精确时间窗，例如最后 N 分钟 |
| `downloadActivityFitFiles` | 下载一个或多个活动的 FIT 文件，可按活动或日期范围 |
| `queryActivityFitFileDownloadUrls` | 在客户端不能接收二进制文件时获取 FIT 下载链接 |

FIT 本体下载和链接查询共用固定 24 小时内 50 个文件的额度。

## 健康与恢复

| 工具 | 用途 |
| --- | --- |
| `queryDailyHealthData` | 每日步数、卡路里、压力、睡眠和心率概览 |
| `querySleepData` | 睡眠评分、主睡眠、深睡、浅睡、REM、清醒、睡眠窗口和小睡 |
| `querySleepHrv` | 睡眠 HRV 的官方评估和原始曲线；日均值与正常范围以官方评估为准 |
| `queryAvgHeartRate` | 每日平均心率趋势 |
| `queryRestingHeartRate` | 每日静息心率趋势 |
| `queryStressLevel` | 每日平均压力趋势 |
| `queryHealthCheckTimeSeries` | 健康快测曲线：心率、HRV、压力、呼吸率、血氧 |
| `queryStressTimeSeries` | 压力原始点，含时间、压力值、展示分、压力 HRV 和压力心率 |
| `queryRecoveryStatus` | 当前恢复百分比、恢复等级和预计完全恢复时间 |
| `queryMenstruationCycles` | 生理周期、今日状态、下次经期和阶段 |

只问心率时用心率专项工具。健康快测的“最近几天”模式和压力原始曲线通常最多 7 天，明确日期范围是否可以更长以工具定义为准。

## 训练

| 工具 | 用途 |
| --- | --- |
| `queryFitnessAssessmentOverview` | VO2max、跑力、阈值配速，以及 5 公里、10 公里、半马、全马预测 |
| `queryTrainingLoadAssessment` | 近期每日评语、短期负荷、长期负荷和负荷比 |
| `queryTrainingSchedule` | 本周或指定日期的日程；修改前区分计划课程和独立排期 |
| `queryTrainingPlanLibrary` | 按状态和类型列出训练计划，以及是否可编辑 |
| `queryTrainingPlanDetails` | 读取计划及其课程结构 |
| `createTrainingPlan` | 创建 4 到 16 个自然周的跑步、骑行或越野计划 |
| `updateTrainingPlan` | 替换进行中执行计划里被提交日期的全天课程 |
| `queryWorkoutLibrary` | 列出课程库中的可复用课程 |
| `queryWorkoutDetails` | 读取课程库模板内容和可编辑状态 |
| `createSingleWorkout` | 只保存到课程库，不安排日期 |
| `updateWorkoutDetails` | 替换课程库模板，不影响已排期副本 |
| `scheduleWorkout` | 把库中已有课程复制到某一天，库原件不变 |
| `createScheduledWorkout` | 在某一天直接新建跑步、骑行或越野课，不加入课程库 |
| `queryScheduledWorkoutDetails` | 按日期和日程副本编号读取独立排期课程 |
| `updateScheduledWorkout` | 替换某一天可编辑的独立排期课程 |

## 其他

| 工具 | 用途 |
| --- | --- |
| `queryDevices` | 已绑定设备的 ID、固件类型和自定义名称 |
| `queryUserInfo` | 身高、体重、生日和性别 |

## 官方限制

- 每次授权只覆盖当前用户自己的数据。
- 没有 Webhook，也不能在这里导入或导出 GPX。
- 运动记录不能双向同步回其他平台。
- 独立日程的移动和删除、训练计划的退出和删除，需要在 COROS App 完成。
