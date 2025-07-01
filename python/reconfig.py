import re
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../rustdesk/libs/hbb_common/src/config.rs')

with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# 替换 RENDEZVOUS_SERVERS
modified_content, count_rendezvous = re.subn(
    r'pub\s+const\s+RENDEZVOUS_SERVERS\s*:\s*&\[&str\]\s*=\s*&\[\s*"rs-ny\.rustdesk\.com"\s*\];',
    'pub const RENDEZVOUS_SERVERS: &[&str] = &["rd.1128.pp.ua"];',
    content,
    flags=re.DOTALL
)

# 替换 RS_PUB_KEY
modified_content, count_pubkey = re.subn(
    r'pub\s+const\s+RS_PUB_KEY\s*:\s*&str\s*=\s*"OeVuKk5nlHiXp\+APNn0Y3pC1Iwpwn44JGqrQCsWqmBw="\s*;',
    'pub const RS_PUB_KEY: &str = "0TyH5O6BjoRmefYCsRDMxiskEDPry25MSMPkc9mIlkw=";',
    modified_content,
    flags=re.DOTALL
)

print(f"[DEBUG] RENDEZVOUS_SERVERS 替换次数: {count_rendezvous}")
print(f"[DEBUG] RS_PUB_KEY 替换次数: {count_pubkey}")

with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
    f.write(modified_content)
