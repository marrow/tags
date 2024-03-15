import inspect

from copy import deepcopy

from marrow.util.compat import IO
from marrow.util.object import NoDefault
from marrow.tags.util import quoteattrs, escape


__all__ = ['Fragment', 'Tag', 'Text', 'AutoTag', 'tag']



class Fragment(object):
	def __init__(self, data=None, *args, **kw):
		self.args = list(args)
		self.attrs = kw
		self.data = data
		
		super(Fragment, self).__init__()
	
	def __repr__(self):
		return "<%s args=%r attrs=%r>" % (self.name, self.args, self.attrs)
	
	def clear(self):
		self.args = list()
		self.attrs = dict()


class Text(Fragment):
	def __init__(self, data, escape=True, *args, **kw):
		super(Text, self).__init__(data, *args, **kw)
		self.escape = escape
	
	def __iter__(self):
		yield escape(self.data) if self.escape else self.data


class Flush(Fragment):
	def __iter__(self):
		yield ''


class Tag(Fragment):
	def __init__(self, name, prefix=None, simple=False, strip=False, *args, **kw):
		super(Tag, self).__init__([], *args, **kw)
		
		self.name = name
		
		self.prefix = prefix
		self.simple = simple
		self.strip = strip
	
	def __call__(self, strip=NoDefault, *args, **kw):
		self = deepcopy(self)
		
		if strip is not NoDefault: self.strip = strip
		self.args.extend(list(args))
		self.attrs.update(kw)
		
		return self
	
	def __getitem__(self, k):
		if not k: return self
		
		self = deepcopy(self)
		
		if not isinstance(k, (tuple, list)):
			k = (k, )
		
		for fragment in k:
			if isinstance(fragment, str):
				self.data.append(escape(fragment))
				continue
			
			self.data.append(fragment)
		
		return self
	
	def __repr__(self):
		return "<%s children=%d args=%r attrs=%r>" % (self.name, len(self.data), self.args, self.attrs)
	
	def __unicode__(self):
		"""Return a serialized version of this tree/branch."""
		
		return u''.join(str(i) for i in self)
	
	__str__ = __unicode__
	
	def render(self):
		buf = u""
		
		for chunk in self:
			if not chunk:
				yield buf
				buf = u""
				continue
			
			buf += chunk
		
		# Handle the remaining data.
		if buf:
			yield buf
	
	def __copy__(self):
		return Tag(self.name, self.prefix, self.simple, self.strip, *self.args, **self.attrs)
	
	def __iter__(self):
		if not self.strip:
			if self.prefix:
				yield self.prefix
			
			yield u'<' + self.name + u''.join([attr for attr in quoteattrs(self, self.attrs)]) + u'>'
		
		if self.simple:
			return
		
		for child in self.data:
			if inspect.isgenerator(child):
				for element in child:
					if isinstance(element, str):
						yield element
						continue
					
					for chunk in element:
						yield chunk
				
				continue
			
			if isinstance(child, Fragment):
				for element in child:
					yield element
				
				continue
			
			if inspect.isroutine(child):
				value = child()
				
				if isinstance(value, str):
					yield value
					continue
				
				for element in value:
					yield element
				
				continue
			
			yield child
		
		if not self.strip:
			yield u'</' + self.name + u'>'
	
	def clear(self):
		self.data = []
		super(Tag, self).clear()
	
	def empty(self):
		self.data = []

