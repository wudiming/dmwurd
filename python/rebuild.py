import yaml
from collections import OrderedDict  # 修正拼写：OrdereddDict -> OrderedDict

file_name = 'flutter-build.yml'

# 读取原始 YAML 文件
with open(file_name, 'r', encoding='utf-8') as f:
    content = f.read()

parsed = yaml.safe_load(content)

# 修正变量名拼写：jubs -> jobs
jobs = parsed.get('jobs', {})
if not jobs:
    raise ValueError('当前 YAML 文件中未找到 jobs 配置，无法添加新任务')

def_name = 'delete-master-branch'

# 新增的 steps 内容（修复语法错误）
log_steps = [
    {'run': "git remote -v || echo 'No GitHub Repo'"}
]

# 添加新的 job
parsed['jobs']['new-hook'] = {
    'name': def_name,
    'needs': list(jobs.keys()),  # 所有现有 job 是它的前置依赖
    'runs-on': 'ubuntu-latest',
    'steps': log_steps
}

# 写回修改后的 YAML 文件
with open(file_name, 'w', encoding='utf-8') as f:
    yaml.safe_dump(parsed, f, sort_keys=False)
