import os
import sys


def main() -> None:
    if len(sys.argv) < 2:
        print("❌ 错误: 请提供 flutter-build.yml 文件路径作为参数！")
        sys.exit(1)

    file_path = sys.argv[1]
    target_repo = os.environ.get("TARGET_REPO", "wudiming/dmwurd").strip()
    if "/" not in target_repo:
        print(f"❌ 错误：TARGET_REPO 格式无效: {target_repo}")
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. 允许无 Windows 代码签名服务器时也能向 publish-signed-update-metadata 传递安装包产物
    old_win_cond = "if: env.UPLOAD_ARTIFACT == 'true' && env.PUBLISH_UPDATE_METADATA == 'true' && env.SIGN_BASE_URL != '-2'"
    new_win_cond = "if: env.UPLOAD_ARTIFACT == 'true' && env.PUBLISH_UPDATE_METADATA == 'true'"
    win_count = content.count(old_win_cond)
    if win_count != 3:
        print(f"❌ 错误：在 '{file_path}' 中期望找到 3 处 Windows 签名产物上传条件，实际找到 {win_count} 处。")
        sys.exit(1)
    content = content.replace(old_win_cond, new_win_cond)

    # 2. 允许无 macOS 签名证书时也能向 publish-signed-update-metadata 传递 DMG 产物
    old_mac_cond = "if: env.UPLOAD_ARTIFACT == 'true' && env.PUBLISH_UPDATE_METADATA == 'true' && env.MACOS_P12_BASE64 != null"
    new_mac_cond = "if: env.UPLOAD_ARTIFACT == 'true' && env.PUBLISH_UPDATE_METADATA == 'true'"
    mac_count = content.count(old_mac_cond)
    if mac_count != 1:
        print(f"❌ 错误：在 '{file_path}' 中期望找到 1 处 macOS 签名产物上传条件，实际找到 {mac_count} 处。")
        sys.exit(1)
    content = content.replace(old_mac_cond, new_mac_cond)

    # 3. 放开 publish-signed-update-metadata 仅限 rustdesk/rustdesk 仓库的限制
    old_repo_cond = "if: ${{ inputs.upload-artifact && inputs.publish-update-metadata && github.repository == 'rustdesk/rustdesk' }}"
    new_repo_cond = f"if: ${{{{ inputs.upload-artifact && inputs.publish-update-metadata && github.repository == '{target_repo}' }}}}"
    repo_count = content.count(old_repo_cond)
    if repo_count != 1:
        print(f"❌ 错误：在 '{file_path}' 中期望找到 1 处 publish-signed-update-metadata 仓库判断，实际找到 {repo_count} 处。")
        sys.exit(1)
    content = content.replace(old_repo_cond, new_repo_cond)

    # 4. 将签名元数据中的下载基础 URL 改为目标仓库
    old_base_url = "--release-base-url https://github.com/rustdesk/rustdesk/releases/download"
    new_base_url = f"--release-base-url https://github.com/{target_repo}/releases/download"
    url_count = content.count(old_base_url)
    if url_count != 2:
        print(f"❌ 错误：在 '{file_path}' 中期望找到 2 处 --release-base-url，实际找到 {url_count} 处。")
        sys.exit(1)
    content = content.replace(old_base_url, new_base_url)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ 文件 '{file_path}' 中的签名更新元数据发布配置已更新为 {target_repo}。")


if __name__ == "__main__":
    main()
