from setuptools import setup

setup(name='JAGpy',
      version='0.3',
      packages=['CloneResouceMachine'],
      dependency_links=[
            'https://github.com/SleepyJay/JAGpy',
      ],
      install_requires=[
            'prettytable',
            'JAGpy',
            'PyYAML'
      ],
      )


# description = 'JAGpy Library Code',
# url = 'https://github.com/SleepyJay/JAGpy',
# author = 'SleepyJay',
# author_email = 'sleepyjay@d20green.com',
# packages = [
#                  'JAGpy'
#            ],
# install_requires = [
#                          'JAGpy',
#                    ],
# zip_safe = False)