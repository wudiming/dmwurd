import sys

# 从命令行第一个参数获取文件路径
file_path = sys.argv[1]

# 定义要查找和替换的内容
old_line = "final url = 'https://rustdesk.com/download';"
new_line = "final url = 'https://github.com/wudiming/dmwurd/releases/latest';"

try:
    # --- 读取文件内容 ---
    # 使用 with 语句可以确保文件被正确关闭
    # 指定 utf-8 编码以避免乱码问题
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # --- 检查是否需要修改 ---
    if old_line not in content:
        print(f"🟡 在文件 '{file_path}' 中未找到目标链接，无需修改。")
    else:
        # --- 执行替换 ---
        content = content.replace(old_line, new_line)

        # --- 将修改后的内容写回文件 ---
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # --- 打印成功信息 ---
        print(f"✅ 文件 '{file_path}' 中的下载链接已成功修改。")

except FileNotFoundError:
    print(f"❌ 错误：文件 '{file_path}' 未找到。")
except Exception as e:
    print(f"❌ 处理文件时发生未知错误: {e}")
