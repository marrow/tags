# encoding: utf-8

import sys
import datetime
from collections import defaultdict

# TODO - eliminate the need for pytz
# from pytz import utc

from marrow.util.convert import KeywordProcessor


__all__ = ['TransformException', 'Transform', 'BaseTransform', 'ListTransform', 'TagsTransform', 'IntegerTransform',
           'FloatTransform', 'DateTimeTransform']


if sys.version_info > (3, 0):
    txt_type = str
else:
    txt_type = unicode


class TransformException(Exception):
    """May represent an error validating a field or a
    document containing fields with validation errors.
    :ivar errors: A dictionary of errors for fields within this
        document or list, or None if the error is for an
        individual field.
    """
    # Code copied from mongoengine's ValidationError:
    # https://github.com/MongoEngine/mongoengine/blob/master/mongoengine/errors.py

    errors = {}
    field_name = None
    _message = None
    valid = {}
    invalid = {}

    def __init__(self, message="", **kwargs):
        self.errors = kwargs.get('errors', {})
        self.valid = kwargs.get('valid', {})
        self.invalid = kwargs.get('invalid', {})
        self.field_name = kwargs.get('field_name')
        self.message = message

    def __str__(self):
        return txt_type(self.message)

    def __repr__(self):
        return '%s(%s,)' % (self.__class__.__name__, self.message)

    def __getattribute__(self, name):
        message = super(TransformException, self).__getattribute__(name)
        if name == 'message':
            if self.field_name:
                message = '%s' % message
            if self.errors:
                message = '%s(%s)' % (message, self._format_errors())
        return message

    def _get_message(self):
        return self._message

    def _set_message(self, message):
        self._message = message

    message = property(_get_message, _set_message)

    def to_dict(self):
        """Returns a dictionary of all errors within a document

        Keys are field names or list indices and values are the
        validation error messages, or a nested dictionary of
        errors for an embedded document or list.
        """

        def build_dict(source):
            errors_dict = {}
            if not source:
                return errors_dict
            if isinstance(source, dict):
                for field_name, error in source.items():
                    errors_dict[field_name] = build_dict(error)
            elif isinstance(source, TransformException) and source.errors:
                return build_dict(source.errors)
            else:
                return txt_type(source)
            return errors_dict
        if not self.errors:
            return {}
        return build_dict(self.errors)

    def _format_errors(self):
        """Returns a string listing all errors within a document"""

        def generate_key(value, prefix=''):
            if isinstance(value, list):
                value = ' '.join([generate_key(k) for k in value])
            if isinstance(value, dict):
                value = ' '.join(
                        [generate_key(v, k) for k, v in value.items()])

            results = "%s.%s" % (prefix, value) if prefix else value
            return results

        error_dict = defaultdict(list)
        for k, v in self.to_dict().items():
            error_dict[generate_key(v)].append(k)
        return ' '.join(["%s: %s" % (k, v) for k, v in error_dict.items()])


class Transform(object):
    def __call__(self, value):
        """Convert a value from Python to Web-safe.
        
        Override this in your subclass.
        """
        
        raise NotImplementedError
    
    def native(self, value):
        """Convert a Web-safe value to Python.
        
        Override this in your subclass.
        """
        
        raise NotImplementedError


class BaseTransform(Transform):
    def __call__(self, value):
        if value is None: return u''
        
        try:
            return txt_type(value)
        
        except:
            raise TransformException()
    
    def native(self, value):
        if value == '': return None
        
        if isinstance(value, str):
            return value.decode('utf-8')
        
        return value


class ListTransform(BaseTransform):
    processor = KeywordProcessor(', \t\n', normalize=lambda s: s.strip('"'))
    
    def __init__(self, processor=None):
        if processor is not None: self.processor = processor
    
    def __call__(self, value):
        if value is None: return u''
        
        if not isinstance(value, list):
            raise TransformException()
        
        return txt_type(self.processor(value))
    
    def native(self, value):
        value = super(ListTransform, self).native(value)
        if value is None: return value
        
        return self.processor(value)


class TagsTransform(ListTransform):
    processor = KeywordProcessor(' \t,', normalize=lambda s: s.lower().strip('"'), sort=True, result=list)


class BooleanTransform(Transform):
    def __call__(self, value):
        if value: return 'True'
        return None
    
    def native(self, value):
        if not value: return False
        return True


class IntegerTransform(Transform):
    def __call__(self, value):
        if value is None: return u''
        
        return txt_type(value)
    
    def native(self, value):
        value = value.strip()
        if not value: return None
        
        return int(value)


class FloatTransform(Transform):
    def __call__(self, value):
        if value is None: return u''
        
        return txt_type(value)
    
    def native(self, value):
        value = value.strip()
        if not value: return None
        
        return float(value)


class DateTimeTransform(Transform):
    base = datetime.datetime
    format = "%Y-%m-%d %H:%M:%S"
    
    def __call__(self, value):
        if value is None: return u''
        
        return txt_type(value.strftime(self.format))
    
    def native(self, value):
        value = value.strip()
        if not value: return None
        
        return self.base.strptime(value, self.format)
        
        # TODO
        # return value if value.tzinfo is not None else value.replace(tzinfo=utc)
