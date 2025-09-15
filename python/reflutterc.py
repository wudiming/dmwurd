import sys # 导入 sys 模块

# 从命令行参数获取文件路径
file_path = sys.argv[1]

# 使用传入的文件路径，并统一加上 utf-8 编码
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'upload-artifact: false',
    'upload-artifact: true'
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✅ 文件 '{file_path}' 中 upload-artifact 已修改为: true")
