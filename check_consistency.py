import json, re, pathlib

root = pathlib.Path(__file__).resolve().parent
mcp = json.loads((root / "mcp.json").read_text())
meta = json.loads((root / "connector-meta.json").read_text())

servers = list(mcp["mcpServers"].keys())
skill_txt = (root / "skills/coros-training/SKILL.md").read_text()
fm_block = re.match(r"^---\n(.*?)\n---\n", skill_txt, re.S).group(1)
fm = {}
for line in fm_block.split("\n"):
    if ": " in line and not line.startswith(" "):
        k, v = line.split(": ", 1)
        fm[k] = v

skill_dir = (root / "skills/coros-training").name
srv = mcp["mcpServers"][servers[0]]

checks = [
    ("mcp server key", servers[0]),
    ("meta source", meta["source"]),
    ("skill name", fm["name"]),
    ("skills 目录名", skill_dir),
]
print("=== 标识一致性 ===")
for label, val in checks:
    print(f"{label:<16}: {val}")
print()
print("四处一致      :", len({v for _, v in checks}) == 1 and len(servers) == 1)
print("server 数量为 1 :", len(servers) == 1)
print("无凭据字段     :", not re.search(r"token|secret|password", json.dumps(mcp), re.I))
print("url 正确      :", srv["url"] == "https://mcpcn.coros.com/mcp")
print("type 正确     :", srv["type"] == "streamableHttp")
print("timeout 保留  :", srv.get("timeout") == 30000)
print("display_name  :", fm["display_name"])