#   Copyright 2012 UFRGS
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from setuptools import setup,find_packages

setup (
  name = 'ProViNet',
  version = '0.1',
  packages = find_packages(),

  # Declare your packages' dependencies here, for eg:
  install_requires=['foo>=3'],

  # Fill in these to make your Egg ready for upload to
  # PyPI
  author = 'wpjesus,sandbc',
  author_email = '',

  summary = 'ProViNet is a Open Platform for Programmable Virtual Network Management and Network Programming',
  url = 'https://github.com/wpjesus/ProViNet',
  license = 'Apache License, Version 2.0',
  long_description= 'For more informations access http://futureinternet.br/provinet',

  # could also include long_description, download_url, classifiers, etc.

  
)