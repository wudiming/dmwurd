import os
import re
import sys

try:
    tag = os.environ["remote_tag"]
except KeyError:
    print("❌ 错误: 环境变量 remote_tag 未设置，无法继续！")
    sys.exit(1)

if len(sys.argv) < 2:
    print("❌ 错误: 请提供要修改的 workflow 文件路径作为参数！")
    sys.exit(1)
file_path = sys.argv[1]

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'upload-artifact: false' not in content and 'upload-artifact: true' not in content:
        print(f"❌ 错误: 在 '{file_path}' 中未找到 'upload-artifact' 配置。")
        sys.exit(1)

    # 必须为可复用 workflow 添加 secrets: inherit，否则 flutter-build.yml 无法读取 RUSTDESK_UPDATE_ED25519_SEED
    if 'secrets:' not in content:
        uses_pattern = re.compile(r'([ \t]*)(uses:\s*\./\.github/workflows/flutter-build\.yml)')
        content, count_secrets = uses_pattern.subn(rf'\1\2\n\1secrets: inherit', content, count=1)
        if count_secrets == 0:
            print(f"❌ 错误: 在 '{file_path}' 中未找到 'uses: ./.github/workflows/flutter-build.yml'，无法添加 'secrets: inherit'。")
            sys.exit(1)

    content = content.replace('upload-artifact: false', 'upload-artifact: true')

    if 'upload-tag:' in content:
        content, count_tag = re.subn(
            r'(upload-tag:\s*)"[^"]*"',
            rf'\1"{tag}"',
            content,
        )
        if count_tag == 0:
            print(f"❌ 错误: 在 '{file_path}' 中替换 'upload-tag' 失败。")
            sys.exit(1)
    else:
        pattern = re.compile(r'([ \t]*)(upload-artifact:\s*true)')
        content, count = pattern.subn(rf'\1\2\n\1upload-tag: "{tag}"', content, count=1)
        if count == 0:
            print(f"❌ 错误: 在 '{file_path}' 中插入 'upload-tag' 失败。")
            sys.exit(1)

    if 'publish-update-metadata:' in content:
        content, count_meta = re.subn(
            r'(publish-update-metadata:\s*)(?:true|false)',
            r'\1true',
            content,
        )
        if count_meta == 0:
            print(f"❌ 错误: 在 '{file_path}' 中替换 'publish-update-metadata' 失败。")
            sys.exit(1)
    else:
        pattern = re.compile(r'([ \t]*)(upload-tag:\s*"[^"]*")')
        content, count = pattern.subn(rf'\1\2\n\1publish-update-metadata: true', content, count=1)
        if count == 0:
            print(f"❌ 错误: 在 '{file_path}' 中插入 'publish-update-metadata' 失败。")
            sys.exit(1)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ 文件 '{file_path}' 中的 CI 工作流参数已成功更新 (secrets=inherit, upload-tag={tag}, publish-update-metadata=true)。")

except FileNotFoundError:
    print(f"❌ 错误：找不到文件 '{file_path}'")
    sys.exit(1)
except Exception as e:
    print(f"❌ 处理文件 '{file_path}' 时发生未知错误: {e}")
    sys.exit(1)
