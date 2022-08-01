# Marrow Tags

[![][latestversion]][latestversion_] [![][ghtag]][ghtag_] [![][masterreq]][masterreq_] [![][ghwatch]][ghsubscription] [![][ghstar]][ghsubscription]

> © 2010-2022 Alice Bevan-McGregor and contributors.

> https://github.com/marrow/tags

An object-based template and widget library wherein templates are interpreted by Python itself.


## Contents

1. [Overview](#overview)

2. [Installation](#installation)

   1. [Development Version](#development-version)

3. [Getting Started](#getting-started)

4. [Version History](#version-history)

5. [License](#license)


## Overview

The `marrow.tags` package offers highly efficient, customizable pure-Python HTML (XML, and other) text generation, and a library of small reusable "widgets".  The following are a list of features:

* No additional languages to learn: it's all Python.
  * You benefit from Python's opcode generation and caching systems.
  * Compatible with all Python interpreters: CPython, Jython, Pypy, IronPython, etc.
* Usable as a templating engine:
  * Extremely light-weight.
  * Utilizes Python's existing package management infrastructure.
* Generated text is optionally beautifully indented and clean.
  * May also be optimized if the given markup supports element elision, such as HTML.
* Out-of-the-box support for pipe-based filters.
* Plays well with others: templates (and widgets) can be treated as Unicode strings, and MarkupSafe protocols are supported.
* Fully unit tested.
* Compatible with Python 2.6+ and 3.1+.



## Installation

Installing `marrow.tags` is easy, just execute the following in a terminal:

	pip install marrow.tags

**Note:** We *strongly* recommend always using a container, virtualization, or sandboxing environment of some kind when developing using Python. We highly recommend use of the Python standard [`venv` (_"virtual environment"_) mechanism][venv].

If you add `marrow.tags` to the `install_requires` argument of the call to `setup()` in your application's `setup.py` or `setup.cfg` files, Marrow Tags will be automatically installed and made available when your own application or library is installed. Use `marrow.tags ~= 1.0.0` to get all bug fixes for the current release while ensuring that large breaking changes are not installed by limiting to the same major/minor, >= the given patch level.


### Development Version

> [![][developcover]][developcover_] [![][ghsince]][ghsince_] [![][ghissues]][ghissues_] [![][ghfork]][ghfork_]

Development takes place on [GitHub][github] in the [tags][repo] project. Issue tracking, documentation, and downloads are provided there.

Installing the current development version requires [Git][git]), a distributed source code management system. If you have Git you can run the following to download and *link* the development version into your Python runtime:

	git clone https://github.com/marrow/tags.git
	pip install -e 'tags[development]'

You can then upgrade to the latest version at any time, from within that source folder:

	git pull
	pip install -e '.[development]'

If you would like to make changes and contribute them back to the project, fork the GitHub project, make your changes, and submit a pull request. This process is beyond the scope of this documentation; for more information see [GitHub's documentation][ghhelp].



## Getting Started

This library is… unusual. Some metaprogramming tricks have been used to permit the dynamic _factory construction_ of new Tag subclasses on attribute access. This process can be interposed to specialize specific tags, or elements, through the use of namespaced "Python entry points" plugins.

If you're utilizing basic XML, the base `Tag` class may be enough for you by permitting dynamic construction of new `Tag` subclasses. Import the `Tag` class and get cracking!

```python
from marrow.tags import Tag


elements = Tag.document ( lang = 'en' ) [
		Tag.element ( id_ = 'first' ) [ "I'm the first element of this document!" ]
	]

print(elements)
```

The above code should result in the following XML-ish output:

```
<document lang="en">
	<element id="first">I'm the first element of this document!</element>
</document>
```

A shortcut is provided; the `marrow.tags` "module"... isn't, strangely. It's actually `Tag` itself! This permits you to import tags directly from the "module", which will construct them dynamically at import time. Case is relatively unimportant, so for clarity we'll import these with class-like capitalization. Other than being shorter, this example is identical to the last:

```python
from marrow.tags import Document, Element

elements = Document ( lang = 'en' ) [
		Element ( id_ = 'first' ) [ "I'm the first element of this document!" ]
	]

print(elements)
```

## Version History

This project has yet to make any releases. When it does, each release should be documented here with a sub-section for the version, and a bulleted list of itemized changes tagged with the kind of change, e.g. *fixed*, *added*, *removed*, or *deprecated*.


## License

Marrow Tags has been released under the MIT Open Source license.

### The MIT License

Copyright © 2010-2022 Alice Bevan-McGregor and contributors.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


[venv]: https://docs.python.org/3/tutorial/venv.html

[git]: http://git-scm.com/
[repo]: https://github.com/marrow/tags/
[github]: https://github.com/
[ghhelp]: https://help.github.com/


[ghwatch]: https://img.shields.io/github/watchers/marrow/tags.svg?style=social&label=Watch "Subscribe to project activity on GitHub."
[ghstar]: https://img.shields.io/github/stars/marrow/tags.svg?style=social&label=Star "Star this project on GitHub."
[ghsubscription]: https://github.com/marrow/tags/subscription
[ghfork]: https://img.shields.io/github/forks/marrow/tags.svg?style=social&label=Fork "Fork this project on Github."
[ghfork_]: https://github.com/marrow/tags/fork

[mastercover]: http://img.shields.io/codecov/c/github/marrow/tags/master.svg?style=flat "Production test coverage."
[mastercover_]: https://codecov.io/github/marrow/tags?branch=master
[masterreq]: https://img.shields.io/requires/github/marrow/tags.svg "Status of production dependencies."
[masterreq_]: https://requires.io/github/marrow/tags/requirements/?branch=master

[developcover]: http://img.shields.io/codecov/c/github/marrow/tags/develop.svg?style=flat "Development test coverage."
[developcover_]: https://codecov.io/github/marrow/tags?branch=develop
[developreq]: https://img.shields.io/requires/github/marrow/tags.svg "Status of development dependencies."
[developreq_]: https://requires.io/github/marrow/tags/requirements/?branch=develop

[ghissues]: http://img.shields.io/github/issues-raw/marrow/tags.svg?style=flat "Github Issues"
[ghissues_]: https://github.com/marrow/tags/issues
[ghsince]: https://img.shields.io/github/commits-since/marrow/tags/1.0.0.svg "Changes since last release."
[ghsince_]: https://github.com/marrow/tags/commits/develop
[ghtag]: https://img.shields.io/github/tag/marrow/tags.svg "Latest Github tagged release."
[ghtag_]: https://github.com/marrow/tags/tree/1.0.0
[latestversion]: http://img.shields.io/pypi/v/marrow.tags.svg?style=flat "Latest released version on Pypi."
[latestversion_]: https://pypi.python.org/pypi/marrow.tags

[cake]: http://img.shields.io/badge/cake-lie-1b87fb.svg?style=flat

