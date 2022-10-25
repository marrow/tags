import inspect

from collections.abc import Collection
from copy import deepcopy
from html import escape
from re import compile as re
from textwrap import indent
from typing import Any, Dict, Iterable, List, Optional, Set, Type, TypeVar, Union
from xml.sax.saxutils import quoteattr


__all__ = ['camel', 'T', 'Fragment', 'Tag', 'Text', 'AutoTag', 'tag']

camel = lambda s: (m.group(0).lower() for m in camel.pattern.finditer(s))
camel.pattern = re('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)')


class T:
	"""The base class encapsulating fundamental tag-based text markup operation."""
	
	localName: Optional[str] = None  # https://developer.mozilla.org/en-US/docs/Web/API/Element/localName
	children: List[Union['T', str]]  # https://developer.mozilla.org/en-US/docs/Web/API/Element/children
	classList: Set[str]  # https://developer.mozilla.org/en-US/docs/Web/API/Element/classList
	attributes: dict[str, str] = {  # https://developer.mozilla.org/en-US/docs/Web/API/Element/attributes
			'class': 'classList',  # https://developer.mozilla.org/en-US/docs/Web/API/Element/classList
		}
	
	_inline = {
			'a', 'abbr', 'acronym', 'audio', 'b', 'bdi', 'bdo', 'big', 'button', 'canvas', 'cite', 'code', 'data',
			'datalist', 'del', 'dfn', 'em', 'embed', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'map',
			'mark', 'meter', 'object', 'output', 'picture', 'progress', 'q', 'ruby', 's', 'samp', 'script', 'select',
			'slot', 'small', 'span', 'strong', 'sub', 'sup', 'svg', 'textarea', 'time', 'title', 'u', 'tt', 'var',
			'wbr'
		}
	
	_void = {'area', 'base', 'br', 'col', 'embed', 'hr', 'iframe', 'img', 'input', 'link', 'meta', 'param', 'portal',
			'source', 'track', 'wbr'}
	
	def __init__(self, name:str, children:Optional[List]=None, **kw) -> None:
		if name in self._void and children:
			raise ValueError("Void elements may not have children.")
		
		self.localName = name
		self.children = children or []  # Populate empty defaults.
		self.classList = set()
		self.attributes = self.attributes.copy()  # Individual instances may dynamically add new attributes.
		
		for name, value in kw.items():
			setattr(self, name, value)
	
	def __repr__(self) -> str:
		return f"<tag '{self.localName}' children={len(self)}{' ' if self.attributes else ''}{self.attributeMapping}>"
	
	def __len__(self) -> int:
		"""Our length is that of the number of our child elements."""
		return len(self.children)
	
	def __iter__(self) -> Iterable[Union[str, 'T']]:
		"""Act as if we are our collection of children when iterated."""
		return iter(self.children)
	
	def __str__(self) -> str:
		parts = []  # These are the string fragments that will ultimately be returned as one.
		parts.extend(('<', self.localName))
		block = self.localName not in self._inline
		
		for key, value in sorted(self.attributeMapping.items()):
			if key[0] == '_': continue  # Armour against protected attribute access.
			
			# Skip values that are non-zero falsy, working around the fact that False == 0.
			if not value and (value is False or value != 0):
				continue
			
			name = str(key).rstrip('_').replace('__', ':').replace('_', '-')
			
			# Add spacer if needed.
			if len(parts) == 2:
				parts.append(' ')
			
			if value is True:  # For explicitly True values, don't emit a value for the attribute.
				parts.append(name)
				continue
			
			# Non-string iterables (such as lists, sets, tuples, etc.) are treated as space-separated strings.
			if isinstance(value, Iterable) and not isinstance(value, str):
				value = " ".join(str(i) for i in value)
			
			value = quoteattr(str(value))
			if " " not in value:
				value = value.strip('"')
			
			parts.extend((name, "=", value))
		
		parts.append('>')
		
		if self.children:
			if __debug__ and block:
				# Prettier "linted" output when optimizations aren't enabled.
				parts.append("\n")
				parts.append(indent("".join(str(child) for child in self), "\t"))
				parts.append("\n")
			else:
				parts.extend(str(child) for child in self)
		
		if self.localName not in self._void:
			parts.extend(('</', self.localName, '>\n' if __debug__ and block else '>'))
		
		return ''.join(parts)
		
		# Three different possible "null" / "empty" scenarios.
		#return f'<{self.localName}></{self.localName}>' + "\n" if __debug__ else ""  # Missing contents.
		#return f'<{self.localName}>'  # HTML5-like self-closing tag.
		#return f'<{self.localName} />'  # XML-like explicit NULL element.
	
	def __len__(self) -> int:
		return len(self.children)
	
	@property
	def attributeMapping(self) -> dict[str, str]:
		return {k: v for k, v in {name: getattr(self, origin, None) for name, origin in self.attributes.items()}.items() if v}
	
	# API-conformant aliases for "localName".
	tagName = \
	nodeName = \
		property(lambda self: self.localName)



if __name__ == '__main__':
	print(T)
	print(repr(T('html')), T('html'), sep="\t")
	print(repr(T('p')), T('p'), sep="\t")
	
	ex = T('p', ['Lorem ipsum dolor...'], classList={'example'})
	print(repr(ex), ex, sep="\n")
	print(ex.attributeMapping)
	
	page = T('html', [
			T('head', [
				T('title', ["Welcome"])
			]),
			T('body', [
				T('p', ["Lorem ipsum dolor sit amet…"])
			]),
		])
	
	print("", repr(page), "", page, sep="\n")
	print("---\n")




class TagMeta(type):
	def __new__(meta, name, bases, attrs):
		cls = type.__new__(meta, str(name), bases, attrs)
		return cls
	
	@property
	def __subclass_map__(Tag):
		return {subclass.__name__: subclass for subclass in Tag.__subclasses__()}
	
	def __getattr__(Tag, name:str):
		localName = '-'.join(camel(name))
		name = name[0].upper() + name[1:]
		
		Tag = Tag.__subclass_map__.get(name, Tag)
		
		return Tag(localName)







class Tag(T, metaclass=TagMeta):
	def __call__(self, **attributes) -> T:
		"""Produce a new, cloned and mutated instance of this tag incorporating attribute changes."""
		instance = self.__class__(self.localName, self.children)  # Mutant pools children!
		instance.__dict__ = self.__dict__.copy()  # It pools all mutable attributes!
		
		for name, value in attributes.items():
			setattr(instance, name, value)
		
		return instance
	
	def __getitem__(self, children) -> T:
		"""Mutate this instance to add these children, returning this instance for chained manipulation."""
		if isinstance(children, (tuple, list)):
			self.children.extend(children)
		else:
			self.children.append(children)
		
		return self
	
	def render(self, encoding=None):
		buf = ""
		
		for chunk in self:
			if not chunk:
				yield buf.encode(encoding) if encoding else buf
				buf = ""
				continue
			
			buf += str(chunk)
		
		# Handle the remaining data.
		if buf:
			yield buf.encode(encoding) if encoding else buf


if __name__ == '__main__':
	print(repr(Tag))
	print(repr(Tag.title))
	print(Tag.title)
	print(Tag.fileUpload)
	print("---\n")
	
	bdole = Tag.p(classList={'name'})["Bob Dole"]
	print(bdole, bdole.__dict__, "", sep="\n")
	print(Tag.p(classList={'fancy', 'wau'})["Much content, super elide."])
	print("---\n")
	
	page = Tag.html [
			Tag.head [
				Tag.title ["Welcome"]
			],
			Tag.body [
				Tag.p ["Lorem ipsum dolor sit amet…"]
			],
		]
	
	print(repr(page), page, sep="\n\n")
	
	feed = Tag.rss[Tag.channel[
		Tag.title["My awesome RSS feed!"],
		Tag.link["https://example.com/"],
		Tag.item["..."]
	]]
	
	print(feed)


# Traits

class _Prefixed:
	"""A generic mix-in to automatically prefix an element with given text."""
	
	prefix: str
	
	def __str__(self):
		return self.prefix + ("\n" if __debug__ else "") + super().__str__()


class _Elidable:
	"""A generic mix-in to override serialization.
	
	If the element would have no attributes, do not render the element at all.
	"""
	
	def __str__(self):
		if not self.classList:
			return "".join(str(child) for child in self)
		
		if __debug__:  # Prettier "linted" output when optimizations aren't enabled.
			parts.append("\n")
			parts.append(indent("".join(str(child) for child in self), "\t"))
		else:
			parts.extend(str(child) for child in self)



class Html(_Prefixed, _Elidable, Tag):
    prefix = "<!DOCTYPE html>"

class Head(_Elidable, Tag): pass
class Body(_Elidable, Tag): pass


if __name__ == '__main__':
	print(Tag.__subclass_map__)
	
	page = Tag.html [
			Tag.head [
				Tag.title [ "I'm really not kidding you." ]
			],
			Tag.body [
				Tag.p [ "This is a complete and fully-formed HTML document." ]
			],
		]
	
	print("""\nTag.html [
        Tag.head [
            Tag.title [ "I'm really not kidding you." ]
        ],
        Tag.body [
            Tag.p [ "This is a complete and fully-formed HTML document." ]
        ],
    ]\n""")
	
	print(page)

