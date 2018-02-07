#!/usr/bin/env python

import os
import versioneer

from codecs import open
from os import environ
from os.path import abspath, dirname, join
from setuptools import setup, find_packages
from sys import version_info, path as sys_path

deps = []

if version_info[0] == 2:
    # Require backport of concurrent.futures on Python 2
    deps.append("futures")

    if version_info[1] < 7 or (version_info[1] == 7 and version_info[2] <= 9):
        deps.append("urllib3[secure]")

# Require singledispatch on Python <3.4
if version_info[0] == 2 or (version_info[0] == 3 and version_info[1] < 4):
    deps.append("singledispatch")

deps.append("requests>=2.2,!=2.12.0,!=2.12.1,!=2.16.0,!=2.16.1,!=2.16.2,!=2.16.3,!=2.16.4,!=2.16.5,!=2.17.1,<3.0")

# for encrypted streams
if environ.get("LIVECLI_USE_PYCRYPTO"):
    deps.append("pycrypto")
elif environ.get("LIVECLI_USE_PYCRYPTODOMEX"):
    deps.append("pycryptodomex>=3.4.3,<4")
else:
    # this version of pycryptodome is known to work and has a Windows wheel for py2.7, py3.3-3.6
    deps.append("pycryptodome>=3.4.3,<4")

# shutil.get_terminal_size and which were added in Python 3.3
if version_info[0] == 2:
    deps.append("backports.shutil_which")
    deps.append("backports.shutil_get_terminal_size")

# for localization
if environ.get("LIVECLI_USE_PYCOUNTRY"):
    deps.append("pycountry")
else:
    deps.append("iso-639")
    deps.append("iso3166")

deps.append("websocket-client")

# Support for SOCKS proxies
deps.append("PySocks!=1.5.7,>=1.5.6")  # requests[socks] uses this version

# win-inet-pton is missing a dependency in PySocks, this has been fixed but not released yet
if os.name == "nt" and version_info < (3, 0):
    # Required due to missing socket.inet_ntop & socket.inet_pton method in Windows Python 2.x
    deps.append("win-inet-pton")

# When we build an egg for the Win32 bootstrap we don't want dependency
# information built into it.
if environ.get("NO_DEPS"):
    deps = []

here = abspath(dirname(__file__))
with open(join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

srcdir = join(dirname(abspath(__file__)), "src/")
sys_path.insert(0, srcdir)

setup(name="livecli",
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      description="Livecli is command-line utility that extracts streams "
                  "from various services and pipes them into a video player of "
                  "your choice.",
      long_description=long_description,
      url="https://github.com/livecli/livecli",
      author="Livecli",
      author_email="backto@protonmail.ch",
      license="Simplified BSD",
      packages=find_packages("src"),
      package_dir={"": "src"},
      entry_points={
          "console_scripts": ["livecli=livecli_cli.main:main"]
      },
      install_requires=deps,
      test_suite="tests",
      classifiers=["Development Status :: 5 - Production/Stable",
                   "Environment :: Console",
                   "Operating System :: POSIX",
                   "Operating System :: Microsoft :: Windows",
                   "Programming Language :: Python :: 2.7",
                   "Programming Language :: Python :: 3.4",
                   "Programming Language :: Python :: 3.5",
                   "Programming Language :: Python :: 3.6",
                   "Programming Language :: Python :: 3.7",
                   "Topic :: Internet :: WWW/HTTP",
                   "Topic :: Multimedia :: Sound/Audio",
                   "Topic :: Multimedia :: Video",
                   "Topic :: Utilities"])
