with open('common.rs', 'r') as f:
    content = f.read()

content = content.replace(
    '"https://admin.rustdesk.com".to_owned()',
    '"https://rd.1128.pp.ua:21114".to_owned()'
)

with open('common.rs', 'w') as f:
    f.write(content)

