#!/usr/bin/env python3

from setuptools import setup, find_packages
from pathlib import Path

here = Path(__file__).resolve().parent
version = None  # Populated by the next line.
exec((here / "marrow" / "tags" / "release.py").read_text('utf-8'))


tests_require = [
		'pytest',  # test collector and extensible runner
		'pytest-runner',  # setuptools test integration
		'pytest-cov',  # coverage reporting
		'pytest-flakes',  # syntax validation
		'pytest-isort',  # import ordering
		'misaka', 'pygments',  # Markdown field support
		'pytz', 'tzlocal>=1.4',  # timezone support, logger support
		'pytest-benchmark',  # automated benchmarking tests
	]


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
		keywords = [],
		
		classifiers = [
				"Development Status :: 1 - Planning",
				"Environment :: Console",
				"Intended Audience :: Developers",
				"License :: OSI Approved :: MIT License",
				"Operating System :: OS Independent",
				"Programming Language :: Python",
				"Topic :: Software Development :: Libraries :: Python Modules"
			],
		
		install_requires = [
			'markupsafe~=2.1.1',  # HTML escaping protocol.
			'typeguard~=2.13.3',  # Strict validation of annotation hints.
		],
		extras_require = dict(
			development = tests_require + ['pre-commit', 'bandit'],  # Development-time dependencies.
		),
		
		packages = find_packages(exclude=['examples', 'tests']),
		include_package_data = True,
		package_data = {'': ['README.textile', 'LICENSE']},
		
		namespace_packages = ['marrow'],
	)

