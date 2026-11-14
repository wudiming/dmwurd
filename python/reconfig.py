import re
import sys

config_path = sys.argv[1]

with open(config_path, 'r', encoding='utf-8') as f:
    content = f.read()

modified_content, count_rendezvous = re.subn(
    r'pub\s+const\s+RENDEZVOUS_SERVERS\s*:\s*&\[&str\]\s*=\s*&\[\s*"rs-ny\.rustdesk\.com"\s*\];',
    'pub const RENDEZVOUS_SERVERS: &[&str] = &["rd.1128.pp.ua"];',
    content,
    flags=re.DOTALL,
)
if count_rendezvous == 0:
    print(f"❌ 错误：在 '{config_path}' 中未找到 RENDEZVOUS_SERVERS。")
    sys.exit(1)

modified_content, count_pubkey = re.subn(
    r'pub\s+const\s+RS_PUB_KEY\s*:\s*&str\s*=\s*"OeVuKk5nlHiXp\+APNn0Y3pC1Iwpwn44JGqrQCsWqmBw="\s*;',
    'pub const RS_PUB_KEY: &str = "0TyH5O6BjoRmefYCsRDMxiskEDPry25MSMPkc9mIlkw=";',
    modified_content,
    flags=re.DOTALL,
)
if count_pubkey == 0:
    print(f"❌ 错误：在 '{config_path}' 中未找到 RS_PUB_KEY。")
    sys.exit(1)

with open(config_path, 'w', encoding='utf-8') as f:
    f.write(modified_content)

print(f"✅ 文件 '{config_path}' 中的服务器地址和公钥已更新。")
