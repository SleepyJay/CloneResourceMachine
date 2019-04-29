
import os
import urllib.request


print(os.getcwd())

if not os.path.exists('JAGpy'):
    os.mkdir('JAGpy')

url = 'https://github.com/SleepyJay/JAGpy/blob/master/README.md'
urllib.request.urlretrieve(url, os.path.join(os.getcwd(), 'JAGpy', 'README.md'))

os.system('pip install -r requirements.txt')




