# encoding: utf-8

from marrow.util.object import NoDefault


__all__ = ['quoteattrs', 'escape']



def quoteattrs(context, attrs):
    """Escape and quote a dict of attribute/value pairs.
    
    Escape &, <, and > in a string of data, then quote it for use as
    an attribute value.  The " character will be escaped as well.
    Also filter out None values.
    """
    for a, v in attrs.items():
        if v is None or v is NoDefault:
            continue
        
        if callable(v):
            v = v(context)
        
        if isinstance(v, bool):
            if v:
                yield ' ' + a.strip(u'_')
            
            continue
        
        if not isinstance(v, unicode):
            v = unicode(v)
        
        yield ' '  + a.strip(u'_').replace('_', '-') + '="'
        
        for s, r in [(u'&', u"&amp;"), (u">", u"&gt;"), (u"<", u"&lt;"), (u'"', u"&quot;")]:
            try:
                v = v.replace(s, r)
            
            except AttributeError:
                raise AttributeError('Argument %s of %r can not be quoted.' % (a, context))
        
        yield v + '"'


def escape(v):
    """Escape &, <, and > in a string of data."""
    for s, r in [(u'&', u"&amp;"), (u">", u"&gt;"), (u"<", u"&lt;")]:
        v = v.replace(s, r)
    
    return v
