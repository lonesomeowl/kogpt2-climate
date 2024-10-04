import os
print(os.environ['HOME'])
env_key = os.environ.get('DATA_GO_KR_KEY', '')
print(env_key)
