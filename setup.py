# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is mozconfigwrapper.
#
# The Initial Developer of the Original Code is
#  Mozilla Corporation
# Portions created by the Initial Developer are Copyright (C) 2008
# the Initial Developer. All Rights Reserved.
#
# Contributor(s):
#  Andrew Halberstadt <halbersa@gmail.com>
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****

import os
from setuptools import setup, find_packages

PACKAGE_NAME = "mozconfigwrapper"
PACKAGE_VERSION = "0.2"

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
      license='MPL 1.1/GPL 2.0/LGPL 2.1',
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
