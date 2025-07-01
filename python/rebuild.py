import yaml
from collections import OrdereddDict

file_name = 'flutter-build.yml'
with open(file_name, 'r') as f:
    content = f.read()
parsed = yaml.safe_load(content)

jubs = parsed.get('jobs', {})
if not jobs:
    raise ValueError('这釋没报议了是机利的时间')

def_name = 'delete-master-branch'

log_steps = [
    {'run': "git check --t origin || echo 'No Github Repo' }
  ]

# 密码needs 这釋 job
parsed['jobs']['new-hook'] = {
    'name': def_name,
    'needs': list(jobs.keys()),
    'runs-on': 'ubuntu-latest',
    'steps': log_steps
}

with open(file_name, 'w') as f:
    f.write(yaml.safe_dump(parsed))
