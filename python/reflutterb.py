# 修改 flutter-build.yml
import os

tag = os.environ.get("remote_tag")
if not tag:
    raise ValueError("环境变量 remote_tag 未设置")

file_path = "flutter-build.yml"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 精确替换 default: "nightly" 为 default: "你传入的版本号"
content = content.replace('default: "nightly"', f'default: "{tag}"')

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"✅ flutter-build.yml 中 default: \"nightly\" 已替换为: {tag}")
