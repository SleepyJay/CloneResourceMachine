
# This is a quick-and-dirty way to get JAGpy common code here.
# # It's not a great solution in the way that it doing "fake" packaging, but...
# it works and is simple enough to manage for my own personal projects. So, that's a win.

import os
import urllib.request

this_project_uses = ['Pyrove', 'Numbers', 'Structs']
base_url = 'https://raw.githubusercontent.com/SleepyJay/JAGpy/master/JAGpy'

if not os.path.exists('JAGpy'):
    os.mkdir('JAGpy')

for module in this_project_uses:
    name = module + '.py'
    url = os.path.join(base_url, name)
    urllib.request.urlretrieve(url, os.path.join('', 'JAGpy', name))