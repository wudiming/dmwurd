with open('common.rs', 'r') as f:
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

with open('common.rs', 'w') as f:
    f.write(content)

