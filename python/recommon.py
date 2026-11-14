import os
import re
import sys

file_path = sys.argv[1]
target_repo = os.environ.get("TARGET_REPO", "wudiming/dmwurd").strip()
if "/" not in target_repo:
    print(f"❌ 错误：TARGET_REPO 格式无效: {target_repo}")
    sys.exit(1)
owner, repo = target_repo.split("/", 1)

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 允许 release_id_from_update_url 同时识别上游和自定义仓库的 release tag URL
release_match_pattern = re.compile(
    r'let\s+release_id\s*=\s*match\s+segments\.as_slice\(\)\s*\{\s*'
    r'\["rustdesk",\s*"rustdesk",\s*"releases",\s*"tag",\s*release_id\]\s*=>\s*\*release_id,\s*'
    r'\["rustdesk",\s*"rustdesk",\s*"releases",\s*"tag",\s*release_id,\s*""\]\s*=>\s*\*release_id,',
    re.MULTILINE,
)
release_match_replacement = (
    'let release_id = match segments.as_slice() {\n'
    '        ["rustdesk", "rustdesk", "releases", "tag", release_id]\n'
    '        | ["rustdesk", "rustdesk", "releases", "tag", release_id, ""]\n'
    f'        | ["{owner}", "{repo}", "releases", "tag", release_id]\n'
    f'        | ["{owner}", "{repo}", "releases", "tag", release_id, ""] => *release_id,'
)
content, count_release_match = release_match_pattern.subn(release_match_replacement, content, count=1)
if count_release_match != 1:
    print(f"❌ 错误：在 '{file_path}' 中未找到 release_id_from_update_url 的匹配模式。")
    sys.exit(1)

# 2. 将更新检查返回 URL 中的仓库替换为目标仓库
old_line = "let response_url = resp.url;"
if old_line not in content:
    print(f"❌ 错误：在 '{file_path}' 中未找到 '{old_line}'。")
    sys.exit(1)
new_lines = (
    "let mut response_url = resp.url;\n"
    "    response_url = response_url.replace(\n"
    '        "github.com/rustdesk/rustdesk",\n'
    f'        "github.com/{target_repo}"\n'
    "    );"
)
content = content.replace(old_line, new_lines, 1)

# 3. 替换默认 API 服务器地址
old_api = '"https://admin.rustdesk.com".to_owned()'
if old_api not in content:
    print(f"❌ 错误：在 '{file_path}' 中未找到 '{old_api}'。")
    sys.exit(1)
content = content.replace(
    old_api,
    '"https://rd.1128.pp.ua:21114".to_owned()',
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✅ 文件 '{file_path}' 中的更新检查校验、更新链接和 API 地址已修改。")
