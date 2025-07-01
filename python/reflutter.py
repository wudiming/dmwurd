with open('flutter-ci.yml', 'r') as f:
    content = f.read()

content = content.replace(
    'upload-artifact: false',
    'upload-artifact: true'
)

with open('flutter-ci.yml', 'w') as f:
    f.write(content)
