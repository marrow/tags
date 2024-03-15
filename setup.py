#!/usr/bin/env python
# encoding: utf-8

import os
import sys

from setuptools import setup


if sys.version_info < (2, 6):
	raise SystemExit("Python 2.6 or later is required.")

exec(open(os.path.join("marrow", "tags", "release.py")).read())



setup(
		name = "marrow.tags",
		version = version,
		
		description = "An object-based template and widget library wherein templates are interpreted by Python itself.",
		long_description = """\
For full documentation, see the README.textile file present in the package,
or view it online on the GitHub project page:

https://github.com/marrow/marrow.tags""",
		
		author = "Alice Bevan-McGregor",
		author_email = "alice+marrow@gothcandy.com",
		url = "https://github.com/marrow/marrow.tags",
		license = "MIT",
		
		install_requires = [
			'marrow.util < 2.0'
		],
		
		test_suite = 'nose.collector',
		tests_require = ['nose', 'coverage'],
		
		classifiers = [
				"Development Status :: 1 - Planning",
				"Environment :: Console",
				"Intended Audience :: Developers",
				"License :: OSI Approved :: MIT License",
				"Operating System :: OS Independent",
				"Programming Language :: Python",
				"Topic :: Internet :: WWW/HTTP :: WSGI",
				"Topic :: Software Development :: Libraries :: Python Modules"
			],
		
		packages = ('marrow.tags', 'marrow.widgets'),
		zip_safe = True,
		include_package_data = True,
		package_data = {'': ['README.textile', 'LICENSE']},
		
		namespace_packages = ['marrow'],
	)
