# 高驰训练 COROS 连接器

WorkBuddy 连接器，采用 MCP + Skill。数据服务使用高驰官方 MCP，用户在 WorkBuddy 里完成 OAuth 授权后，可以用自然语言查询自己的运动和健康数据，并在明确要求后保存训练计划、课程与每日排期。

## 与市场已有连接器的区别

市场上已有的官方连接器只覆盖**读取**能力：运动记录、活动分析、睡眠、心率、HRV、压力、体能评估与训练日程查询。高驰官方 MCP 在 2026 年 9 月 21 日新增了训练计划与课程的创建、修改和排期能力，市场版尚未跟进。

本连接器的 Skill 覆盖官方 MCP 的**全部工具**，包括此前缺失的写入链路：

| 能力 | 市场已有版 | 本连接器 |
| --- | --- | --- |
| 运动、睡眠、恢复、体能等读取 | 有 | 有 |
| 训练计划库与计划详情 | 读日程，不含计划库 | 有 |
| 创建 4 到 16 周训练计划 | 无 | 有 |
| 修改进行中的执行计划 | 无 | 有 |
| 课程库模板的新建与修改 | 无 | 有 |
| 把课程库课程排到某一天 | 无 | 有 |
| 某一天直接新建课程 | 无 | 有 |
| 修改独立排期课程 | 无 | 有 |
| 教练式活动分析、训练负荷评估 | 部分 | 有 |

写入能力统一受一条规则约束：用户只说「建议」「看看怎么练」时只给方案，不落库；明确说保存、创建、安排、修改时才写入，写入前用一句话复述将保存的内容和日期。

## 目录

```text
├── connector-meta.json
├── mcp.json
├── icon.svg
└── skills/coros-training/
    ├── SKILL.md
    └── references/tools.md
```

`mcp.json` 只配置一个 Server，地址为 `https://mcpcn.coros.com/mcp`，传输类型是 `streamableHttp`。未填写 Token。`connector-meta.json` 不设置 `auth_mode`，由 WorkBuddy 按 MCP OAuth 2.1 + PKCE 连接。

当前默认中国大陆节点，因为从大陆访问官方网关时，受保护资源和授权服务器都落在 `mcpcn.coros.com`。高驰不接受 `workbuddy://` 回调，只接受 HTTPS 或本机 `http://127.0.0.1` 回调；WorkBuddy 在私有协议被拒绝后会回退到本机回调。

账号不在中国大陆时，把 `mcp.json` 的 `url` 改成对应节点后重新打包：

| 账号地区 | MCP 地址 |
| --- | --- |
| 中国大陆 | `https://mcpcn.coros.com/mcp` |
| 欧洲 | `https://mcpeu.coros.com/mcp` |
| 美国 | `https://mcpus.coros.com/mcp` |
| 官方全球网关 | `https://mcp.coros.com/mcp` |

全球网关会按账号地区选择节点。客户端若不处理网关返回的资源地址，连接会失败，这时改用上表中的独立节点。

## 能力边界

可以读取运动记录、活动详情、分圈、FIT、睡眠、心率、压力、恢复、体能评估和训练日程，也可以创建或修改跑步、骑行、越野跑的训练计划和课程。

不能接收 Webhook，不能导入导出 GPX，不能把运动记录双向同步到其他平台，也不能在连接器里移动、删除独立日程或退出训练计划。这些限制来自高驰官方 MCP，不是 WorkBuddy 配置可以打开的开关。

## 提交

连接器要求 WorkBuddy 4.24.0 或更高版本。打包时让 `connector-meta.json`、`mcp.json` 和 `icon.svg` 位于压缩包根目录，不要写入任何 Access Token、Client Secret 或账号密码。审核通过后市场上会显示「高驰训练」。

`source` 为 `coros-training`，避开市场已有官方 `coros` 连接器的标识，防止冲突。提交前再次确认该标识仍未被占用。
