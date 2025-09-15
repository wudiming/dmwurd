# 修改 flutter-build.yml
import os
import sys # 导入 sys 模块

# 从命令行参数获取文件路径
file_path = sys.argv[1]

# (这部分逻辑保留) 从环境变量获取 tag
tag = os.environ.get("remote_tag")
if not tag:
    raise ValueError("环境变量 remote_tag 未设置")

# 使用传入的文件路径和 utf-8 编码
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# (这部分逻辑保留) 精确替换版本号
content = content.replace('default: "nightly"', f'default: "{tag}"')

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"✅ 文件 '{file_path}' 中 default: \"nightly\" 已替换为: {tag}")
