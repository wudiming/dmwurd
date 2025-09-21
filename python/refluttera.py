# refluttera.py

import os
import sys
import re

# ==============================================================================
# 步骤 1: 获取输入
# ==============================================================================
try:
    # 从环境变量获取 tag
    tag = os.environ["remote_tag"]
except KeyError:
    print("❌ 错误: 环境变量 remote_tag 未设置，无法继续！")
    sys.exit(1)

# 从命令行参数获取文件路径
if len(sys.argv) < 2:
    print("❌ 错误: 请提供要修改的 workflow 文件路径作为参数！")
    sys.exit(1)
file_path = sys.argv[1]

# ==============================================================================
# 步骤 2: 读取和修改文件内容
# ==============================================================================
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 智能检查：如果 'upload-tag:' 不存在，则添加它
    if 'upload-tag:' not in content:
        # 使用正则表达式找到 'upload-artifact: false' 及其缩进，然后在它下面插入新行
        pattern = re.compile(r"(\s*)(upload-artifact:\s*false)")
        replacement = rf'\g<1>\g<2>\n\g<1>upload-tag: "nightly"'
        
        new_content, count = re.subn(pattern, replacement, content)
        
        if count > 0:
            content = new_content
        else:
            # 如果找不到锚点，这是一个关键错误，应中断执行
            print(f"❌ 错误: 在 '{file_path}' 中未找到 'upload-artifact: false'，无法自动添加 'upload-tag'。")
            sys.exit(1)

    # 执行最终的参数值替换
    # 替换 1: 修改 upload-artifact
    content = content.replace(
        'upload-artifact: false',
        'upload-artifact: true'
    )

    # 替换 2: 修改 upload-tag (无论是预置的还是刚添加的占位符都会被替换)
    content = content.replace(
        'upload-tag: "nightly"',
        f'upload-tag: "{tag}"'
    )

    # 将最终内容写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    # 输出简洁的成功日志
    print(f"✅ 文件 '{file_path}' 中的 CI 工作流参数已成功更新。")

except FileNotFoundError:
    print(f"❌ 错误：找不到文件 '{file_path}'")
    sys.exit(1)
except Exception as e:
    print(f"❌ 处理文件 '{file_path}' 时发生未知错误: {e}")
    sys.exit(1)
