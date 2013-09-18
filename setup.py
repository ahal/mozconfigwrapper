# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
from setuptools import setup, find_packages

PACKAGE_NAME = "mozconfigwrapper"
PACKAGE_VERSION = "0.3"

# take description from README
here = os.path.dirname(os.path.abspath(__file__))
try:
    description = file(os.path.join(here, 'README.md')).read()
except (OSError, IOError):
    description = ''

setup(name=PACKAGE_NAME,
      version=PACKAGE_VERSION,
      description="Utility to make working with mozconfigs easier",
      long_description=description,
      author='Andrew Halberstadt',
      author_email='halbersa@gmail.com',
      url='http://github.com/ahal/mozconfigwrapper',
      license='MPL 2.0/GPL 2.0/LGPL 2.1',
      scripts=['mozconfigwrapper.sh'],
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      entry_points="""
          [console_scripts]
          mozconfig = mozconfigwrapper:mozconfig
        """,
      platforms =['Unix'],
      classifiers=['Development Status :: 3 - Alpha',
                   'Environment :: Console',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: Mozilla Public License 1.1 (MPL 1.1)',
                   'Operating System :: Unix',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                  ]
     )
