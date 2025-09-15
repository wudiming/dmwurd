# prepare_ci_workflow.py

import os
import sys
import re

# ==============================================================================
# 步骤 1: 从环境变量和命令行参数获取输入
# ==============================================================================
# 从环境变量获取 tag
tag = os.environ.get("remote_tag")
if not tag:
    raise ValueError("环境变量 remote_tag 未设置，无法继续！")

# 从命令行参数获取文件路径
if len(sys.argv) < 2:
    raise ValueError("请提供要修改的 workflow 文件路径作为参数！")
file_path = sys.argv[1]

print(f"🚀 开始准备 CI 工作流文件: '{file_path}'")
print(f"   - 使用的版本标签: {tag}")

# ==============================================================================
# 步骤 2: 读取文件并智能处理占位符
# ==============================================================================
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
except FileNotFoundError:
    print(f"❌ 错误：找不到文件 '{file_path}'")
    sys.exit(1)

# 智能检查：如果 'upload-tag:' 不存在，就添加它
if 'upload-tag:' not in content:
    print("   - 未找到 'upload-tag' 参数，准备自动添加占位符...")
    # 使用正则表达式找到 'upload-artifact: false' 及其缩进，然后在它下面插入新行
    # 这确保了缩进的绝对正确
    pattern = re.compile(r"(\s*)(upload-artifact:\s*false)")
    # 替换为原来的行 + 换行 + 带相同缩进的新行
    replacement = rf'\g<1>\g<2>\n\g<1>upload-tag: "nightly"'
    
    new_content, count = re.subn(pattern, replacement, content)
    
    if count > 0:
        content = new_content
        print("   - ✅ 已成功添加 'upload-tag' 占位符。")
    else:
        print(f"   - ⚠️ 警告: 未找到 'upload-artifact: false'，无法自动添加占位符。")
else:
    print("   - 'upload-tag' 参数已存在，无需添加。")

# ==============================================================================
# 步骤 3: 执行最终的参数值替换
# ==============================================================================
print("   - 准备替换参数值为真实值...")

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

# ==============================================================================
# 步骤 4: 将最终内容写回文件
# ==============================================================================
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"🎉 文件 '{file_path}' 已成功更新！")
print(f"   - upload-artifact: true")
print(f"   - upload-tag: \"{tag}\"")
