import re
          with open('config.rs', 'r') as f:
              content = f.read()
          modified_content, count_rendezvous = re.subn(
              r'pub\s+const\s+RENDEZVOUS_SERVERS\s*:\s*&\[&str\]\s*=\s*&\[\s*"rs-ny\.rustdesk\.com"\s*\];',
              'pub const RENDEZVOUS_SERVERS: &[&str] = &["rd.1128.pp.ua"];',
              content,
              flags=re.DOTALL
          )
          modified_content, count_pubkey = re.subn(
              r'pub\s+const\s+RS_PUB_KEY\s*:\s*&str\s*=\s*"OeVuKk5nlHiXp\+APNn0Y3pC1Iwpwn44JGqrQCsWqmBw="\s*;',
              'pub const RS_PUB_KEY: &str = "0TyH5O6BjoRmefYCsRDMxiskEDPry25MSMPkc9mIlkw=";',
              modified_content,
              flags=re.DOTALL
          )
          print(f"[DEBUG] RENDEZVOUS_SERVERS替换次数: {count_rendezvous}")
          print(f"[DEBUG] RS_PUB_KEY替换次数: {count_pubkey}")
          with open('config.rs', 'w') as f:
              f.write(modified_content)
