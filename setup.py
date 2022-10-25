#!/usr/bin/env python3

import os
import sys

from setuptools import setup, find_packages


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
		
		install_requires = [],
		
		classifiers = [
				"Development Status :: 1 - Planning",
				"Environment :: Console",
				"Intended Audience :: Developers",
				"License :: OSI Approved :: MIT License",
				"Operating System :: OS Independent",
				"Programming Language :: Python",
				"Topic :: Software Development :: Libraries :: Python Modules"
			],
		
		packages = find_packages(exclude=['examples', 'tests']),
		include_package_data = True,
		package_data = {'': ['README.textile', 'LICENSE']},
		
		namespace_packages = ['marrow'],
	)
