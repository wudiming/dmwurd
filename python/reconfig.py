import re
import sys

# 从命令行参数获取文件路径
config_path = sys.argv[1]

# 读取文件内容
with open(config_path, 'r', encoding='utf-8') as f:
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

# 写回文件
with open(config_path, 'w', encoding='utf-8') as f:
    f.write(modified_content)

# 使用统一格式的成功输出
print(f"✅ 文件 '{config_path}' 中的服务器地址和公钥已更新。")
