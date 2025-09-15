import sys # 步骤 1：导入 sys 模块

# 步骤 2：从命令行第一个参数获取文件路径
# sys.argv[0] 是脚本名 "recommon.py"
# sys.argv[1] 是我们传入的 "rustdesk/src/common.rs"
file_path = sys.argv[1]

# 步骤 3 & 4：使用 file_path 变量并指定编码
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

# 可以加上一句输出来确认执行成功
print(f"[DEBUG] 文件 '{file_path}' 修改成功。")
