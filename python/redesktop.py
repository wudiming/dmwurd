with open('desktop_home_page.dart', 'r') as f:
              content = f.read()
          # 精确替换目标 URL，保留代码结构
          content = content.replace(
              "launchUrl(Uri.parse('https://rustdesk.com/download'))",
              "launchUrl(Uri.parse('https://github.com/wudiming/dmwurd/releases'))"
          )
          with open('desktop_home_page.dart', 'w') as f:
              f.write(content)
