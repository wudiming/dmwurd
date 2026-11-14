import os
import sys

file_path = sys.argv[1]
target_repo = os.environ.get("TARGET_REPO", "wudiming/dmwurd").strip()
if "/" not in target_repo:
    print(f"❌ 错误：TARGET_REPO 格式无效: {target_repo}")
    sys.exit(1)

old_line = "final Uri url = Uri.parse('https://rustdesk.com/download');"
new_line = f"final Uri url = Uri.parse('https://github.com/{target_repo}/releases/latest');"

old_changelog_prefix = "https://github.com/rustdesk/rustdesk/releases/tag/"
new_changelog_prefix = f"https://github.com/{target_repo}/releases/tag/"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

if old_line not in content:
    print(f"❌ 错误：在文件 '{file_path}' 中未找到目标链接 '{old_line}'。")
    sys.exit(1)
content = content.replace(old_line, new_line)

if old_changelog_prefix not in content:
    print(f"❌ 错误：在文件 '{file_path}' 中未找到 Changelog 链接前缀 '{old_changelog_prefix}'。")
    sys.exit(1)
content = content.replace(old_changelog_prefix, new_changelog_prefix)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✅ 文件 '{file_path}' 中的下载链接与 Changelog 链接已成功修改。")
