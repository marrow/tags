from marrow.tags import filters
from marrow.tags.base import Tag, Flush, Text


__all__ = ['comment', 'html', 'flush', 'Text']


_doctype = '<!DOCTYPE HTML>'
_tags = {'a', 'abbr', 'address', 'area', 'article', 'aside', 'audio', 'b', 'base', 'bdo', 'blockquote', 'body', 'br', 'button', 'canvas', 'caption', 'cite', 'code', 'col', 'colgroup', 'command', 'datalist', 'dd', 'del', 'details', 'dfn', 'div', 'dl', 'dt', 'em', 'embed', 'eventsource', 'fieldset', 'figcaption', 'figure', 'footer', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'head', 'header', 'hgroup', 'hr', 'html', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'keygen', 'label', 'legend', 'li', 'link', 'mark', 'map', 'menu', 'meta', 'meter', 'nav', 'noscript', 'object', 'ol', 'optgroup', 'option', 'output', 'p', 'param', 'pre', 'progress', 'q', 'ruby', 'rp', 'rt', 'samp', 'script', 'section', 'select', 'small', 'source', 'span', 'strong', 'style', 'sub', 'summary', 'sup', 'table', 'tbody', 'td', 'textarea', 'tfoot', 'th', 'thead', 'time', 'title', 'tr', 'ul', 'var', 'video', 'wbr'}
_partial = {'area', 'base', 'br', 'embed', 'eventsource', 'hr', 'img', 'input', 'link', 'meta', 'param', 'wbr', 'source'}
_comment = (u'<!--', u'-->')

# TODO: These are for future optional validation.  I.e. inline elements can not contain block elements, and specific attributes are allowed.
_block = []
_inline = []
_attributes = {'accesskey', 'class', 'contenteditable', 'contextmenu', 'dir', 'draggable', 'hidden', 'id', 'lang', 'spellcheck', 'style', 'tabindex', 'title'}
_events = {'onabort', 'onblur', 'oncanplay', 'oncanplaythrough', 'onchange', 'onclick', 'oncontextmenu', 'ondblclick', 'ondrag', 'ondragend', 'ondragenter', 'ondragleave', 'ondragover', 'ondragstart', 'ondrop', 'ondurationchange', 'onemptied', 'onended', 'onerror', 'onfocus', 'onformchange', 'onforminput', 'oninput', 'oninvalid', 'onkeydown', 'onkeypress', 'onkeyup', 'onload', 'onloadeddata', 'onloadedmetadata', 'onloadstart', 'onmousedown', 'onmousemove', 'onmouseout', 'onmouseover', 'onmouseup', 'onmousewheel', 'onpause', 'onplay', 'onplaying', 'onprogress', 'onratechange', 'onreadystatechange', 'onscroll', 'onseeked', 'onseeking', 'onselect', 'onshow', 'onstalled', 'onsubmit', 'onsuspend', 'ontimeupdate', 'onvolumechange', 'onwaiting'}


flush = Flush()


class comment(Text):
    def __iter__(self):
        yield _comment[0] + self.data + _comment[1]


html = Tag('html', prefix=_doctype)


_locals = locals()
_protected = ('del', )

for t in _tags:
    if t not in _locals:
        _locals[t if t not in _protected else (t + '_')] = Tag(t, simple=t in _partial)
        __all__.append(t if t not in _protected else (t + '_'))

for f in filters.__all__:
    _locals[f] = getattr(filters, f)
    __all__.append(f)

del _locals

