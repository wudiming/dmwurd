import sys

# 从命令行第一个参数获取文件路径
file_path = sys.argv[1]

# 使用 file_path 变量并指定编码
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_line = "let response_url = resp.url;"
new_lines = (
    "    let mut response_url = resp.url;\n"
    "    response_url = response_url.replace(\n"
    "        \"github.com/rustdesk/rustdesk\",\n"
    "        \"github.com/wudiming/dmwurd\"\n"
    "    );"
)
content = content.replace(old_line, new_lines)

content = content.replace(
    '"https://admin.rustdesk.com".to_owned()',
    '"https://rd.1128.pp.ua:21114".to_owned()'
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

# 使用统一格式的成功输出
print(f"✅ 文件 '{file_path}' 中的更新链接和 API 地址已修改。")
