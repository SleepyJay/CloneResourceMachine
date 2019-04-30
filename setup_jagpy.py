
import os
import urllib.request

this_project_uses = ['Numbers', 'Structs']
base_url = 'https://raw.githubusercontent.com/SleepyJay/JAGpy/master/JAGpy'

if not os.path.exists('JAGpy'):
    os.mkdir('JAGpy')

for module in this_project_uses:
    name = module + '.py'
    url = os.path.join(base_url, name)
    urllib.request.urlretrieve(url, os.path.join(os.getcwd(), 'JAGpy', name))