# encoding: utf-8

from copy import deepcopy
from sys import getcheckinterval, setcheckinterval

from marrow.util.compat import IO
from marrow.util.object import NoDefault
from marrow.tags.util import quoteattrs, escape


__all__ = ['Fragment', 'Tag', 'Text', 'AutoTag', 'tag']



class Fragment(object):
    def __init__(self, data_=None, *args, **kw):
        self.args = list(args)
        self.attrs = kw
        self.data = data_
        
        super(Fragment, self).__init__()
    
    def __repr__(self):
        return "<%s args=%r attrs=%r>" % (self.name, self.args, self.attrs)
    
    def clear(self):
        self.args = list()
        self.attrs = dict()


class Tag(Fragment):
    prefix = None
    simple = False
    strip = False
    indent = True
    
    def __init__(self, name=NoDefault, prefix=NoDefault, simple=NoDefault, strip=NoDefault, indent=NoDefault, *args, **kw):
        self.name = self.__class__.__name__ if name is NoDefault else name
        self.children = []
        self.args = list(args)
        self.attrs = kw
        self.data = None
        
        if prefix is not NoDefault: self.prefix = prefix
        if simple is not NoDefault: self.simple = simple
        if strip is not NoDefault: self.strip = strip
        if indent is not NoDefault: self.indent = indent
        
        super(Tag, self).__init__(*args, **kw)
    
    def __call__(self, data_=None, strip=NoDefault, *args, **kw):
        self = deepcopy(self)
        
        self.data = data_
        if strip is not NoDefault: self.strip = strip
        self.args.extend(list(args))
        self.attrs.update(kw)
        
        return self
    
    def __getitem__(self, k):
        if not k: return self
        
        self = deepcopy(self)
        
        if not isinstance(k, (tuple, list)):
            k = [k]
        
        for fragment in k:
            if isinstance(fragment, basestring):
                self.children.append(escape(fragment))
                continue
        
            self.children.append(fragment)
        
        return self
    
    def __repr__(self):
        return "<%s children=%d args=%r attrs=%r>" % (self.name, len(self.children), self.args, self.attrs)
    
    def __unicode__(self):
        """Return a serialized version of this tree/branch."""
        
        # TODO: Determine how badly this effects things.
        ci = getcheckinterval()
        setcheckinterval(0)
        
        value = ''.join(self.render('utf8')).decode('utf8')
        
        setcheckinterval(ci)
        return value
    
    def enter(self):
        if self.strip:
            raise StopIteration()
            
        if self.prefix:
            yield self.prefix
        
        yield u'<' + self.name + u''.join([attr for attr in quoteattrs(self, self.attrs)]) + u'>'
    
    def exit(self):
        if self.simple or self.strip:
            raise StopIteration()
            
        yield u'</' + self.name + u'>'
    
    def render(self, encoding='ascii'):
        indentation = 0
        text = False
        stack = []
        buf = IO()
        
        for k, t in self:
            if k == 'enter':
                indent = getattr(t, 'indent', True)
                
                stack.append(t)
                if t.strip: continue
                
                if text and indent:
                    buf.write('\n')
                
                if indent:
                    buf.write('    ' * indentation)
                
                for element in t.enter():
                    buf.write(element.encode(encoding))
                
                if indent:
                    buf.write('\n')
                    indentation += 1
                
                text = False
                continue
            
            if k == 'exit':
                indent = getattr(t, 'indent', True)
                
                stack.pop()
                if t.strip: continue
                
                if indent:
                    indentation -= 1
                
                if not t.simple:
                    if text and indent: buf.write('\n')
                    if indent: buf.write('    ' * indentation)
                
                for element in t.exit():
                    buf.write(element.encode(encoding))
                
                if not t.simple or t.children: buf.write('\n')
                text = False
                continue
            
            if k == 'text':
                indent = getattr(stack[-1], 'indent', True)
                
                if not text and indent:
                    buf.write('    ' * indentation)
                
                t = t.encode(encoding)
                buf.write(t.replace('\n', '\n' + '    ' * indentation) if indent else t)
                text = True
            
            if k == 'flush':
                yield buf.getvalue()
                del buf
                buf = IO()
        
        yield buf.getvalue()
    
    def __copy__(self):
        t = Tag(self.name, *self.args, **deepcopy(self.attrs))
        t.data = self.data
        t.children = self.children
        return t
    
    def __iter__(self):
        yield 'enter', self
        
        for child in self.children:
            if isinstance(child, Fragment):
                for element in child:
                    yield element
                continue
            
            if hasattr(child, '__call__'):
                value = child(self)
                
                if isinstance(value, basestring):
                    yield 'text', unicode(value)
                    continue
                
                for element in child(self):
                    yield element
                
                continue
            
            yield 'text', unicode(child)
        
        yield 'exit', self
    
    def clear(self):
        self.children = list()
        super(Tag, self).clear()
    
    def empty(self):
        self.children = list()


class Text(Fragment):
    def __init__(self, data=None, escape=True, *args, **kw):
        self.escape = escape
        
        super(Text, self).__init__(data, *args, **kw)
    
    def __iter__(self):
        yield 'text', escape(unicode(self.data)) if self.escape else unicode(self.data)


class Flush(Fragment):
    def __iter__(self):
        yield 'flush', None