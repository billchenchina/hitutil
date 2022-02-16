import pathlib
import sys

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='hitutil',
    version='0.5.0',
    description='hit.edu.cn utils',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/billchenchina/hitutil',
    author='Billchenchina',
    author_email='billchenchina2001@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Natural Language :: Chinese (Simplified)',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Utilities',
    ],
    keywords='Harbin Institute of Technology, HIT, requests',
    package_dir={'': '.'},
    packages=find_packages(where='.'),
    python_requires='>=3.5, <4',
    install_requires=['beautifulsoup4', 'pycryptodome', 'requests', 'pandas'],
    project_urls={
        'Bug Reports': 'https://github.com/billchenchina/hitutil/issues',
        # 'Funding': 'https://donate.pypi.org',
        # 'Say Thanks!': 'http://saythanks.io/to/example',
        'Source': 'https://github.com/billchenchina/hitutil/',
    },
)
