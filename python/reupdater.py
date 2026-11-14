import base64
import binascii
import os
import re
import sys


def decode_public_key(encoded: str) -> list[int]:
    try:
        raw = base64.b64decode(encoded, validate=True)
    except (ValueError, binascii.Error) as err:
        raise ValueError(f"RUSTDESK_UPDATE_ED25519_PUBLIC_KEY Base64 无效: {err}") from err
    if len(raw) != 32:
        raise ValueError(f"RUSTDESK_UPDATE_ED25519_PUBLIC_KEY 解码长度必须为 32 字节，当前为 {len(raw)}")
    if base64.b64encode(raw).decode("ascii") != encoded:
        raise ValueError("RUSTDESK_UPDATE_ED25519_PUBLIC_KEY 必须使用标准 Base64 编码")
    return list(raw)


def patch_artifact_rs(path: str, target_repo: str) -> None:
    owner, repo = target_repo.split("/", 1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    old_prefix = 'format!("https://github.com/rustdesk/rustdesk/releases/download/{release_id}/");'
    new_prefix = f'format!("https://github.com/{target_repo}/releases/download/{{release_id}}/");'
    if old_prefix not in content:
        raise RuntimeError(f"在 '{path}' 中未找到 expected_artifact_url_prefix 定义")
    content = content.replace(old_prefix, new_prefix, 1)

    owner_repo_pattern = re.compile(
        r'if\s+owner\s*!=\s*"rustdesk"\s*\|\|\s*repo\s*!=\s*"rustdesk"',
        re.MULTILINE,
    )
    owner_repo_replacement = (
        f'if !matches!((owner, repo), ("rustdesk", "rustdesk") | ("{owner}", "{repo}"))'
    )
    content, count = owner_repo_pattern.subn(owner_repo_replacement, content, count=1)
    if count != 1:
        raise RuntimeError(f"在 '{path}' 中未找到 get_update_download_file_from_url 的 owner/repo 校验")

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ 文件 '{path}' 中的更新元数据前缀和下载路径校验已更新为 {target_repo}。")


def patch_update_metadata_rs(path: str, pub_bytes: list[int]) -> None:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    key_pattern = re.compile(
        r'(TrustedUpdateKey\s*\{[^{}]*key_id:\s*"2026-ed25519-main"[^{}]*public_key:\s*\[)([^\]]+)(\])',
        re.DOTALL,
    )
    formatted_bytes = ", ".join(str(b) for b in pub_bytes)

    def _replace(match: re.Match[str]) -> str:
        return f"{match.group(1)}\n        {formatted_bytes},\n    {match.group(3)}"

    content, count = key_pattern.subn(_replace, content, count=1)
    if count != 1:
        raise RuntimeError(f"在 '{path}' 中未找到 TRUSTED_UPDATE_KEYS 的 2026-ed25519-main 公钥定义")

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ 文件 '{path}' 中的更新验签公钥已替换为自定义 Ed25519 公钥。")


def main() -> None:
    if len(sys.argv) < 3:
        print("❌ 用法: python3 reupdater.py <artifact.rs> <update_metadata.rs>")
        sys.exit(1)

    artifact_rs_path = sys.argv[1]
    update_metadata_rs_path = sys.argv[2]

    target_repo = os.environ.get("TARGET_REPO", "wudiming/dmwurd").strip()
    if "/" not in target_repo:
        print(f"❌ 错误：TARGET_REPO 格式无效: {target_repo}")
        sys.exit(1)

    pub_b64 = os.environ.get("RUSTDESK_UPDATE_ED25519_PUBLIC_KEY", "").strip()
    if not pub_b64:
        print("❌ 错误：环境变量 RUSTDESK_UPDATE_ED25519_PUBLIC_KEY 未设置！")
        sys.exit(1)

    try:
        pub_bytes = decode_public_key(pub_b64)
        patch_artifact_rs(artifact_rs_path, target_repo)
        patch_update_metadata_rs(update_metadata_rs_path, pub_bytes)
    except Exception as err:
        print(f"❌ 错误：{err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
