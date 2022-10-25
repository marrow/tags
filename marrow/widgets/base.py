import re

from copy import copy
from html import tag

from ..tags.util import Sentinel
from .transforms import BaseTransform, BooleanTransform, TransformException


__all__ = ['Widget', 'NestedWidget', 'Form', 'FieldSet', 'Label', 'Layout', 'Input', 'BooleanInput', 'Link']


class ValidationError(Exception): pass


class Widget:
	transform = BaseTransform()
	default = None
	
	def __init__(self, name_, title_=None, transform=Sentinel, default=Sentinel, data_=Sentinel, **kw):
		self.name = name_
		self.title = title_
		self.data = dict() if data_ is Sentinel else data_
		self.args = kw
		
		if transform is not Sentinel: self.transform = transform
		if default is not Sentinel: self.default = default
	
	@property
	def value(self):
		value = self.data.get(self.name, self.default)
		return self.transform(value) if self.transform else value

	def validate(self, data):
		try:
			self.native(data)
		except Exception as e:
			raise ValidationError(self.name, e)

	def native(self, data):
		value = data.get(self.name, None)
		
		if value is None:
			return self.default
		
		return self.transform.native(value) if self.transform else value

	def _get_error_key(self):
		return self.name
	
	@property
	def template(self):
		raise NotImplementedError
	
	def __call__(self, data=Sentinel):
		local = copy(self) # Thread Safety
		
		if data is not Sentinel:
			if isinstance(local.data, dict) and isinstance(data, dict):
				local.data.update(data)
			
			else:
				local.data = data
		
		return local.template


class NestedWidget(Widget):
	def __init__(self, name_, title_=None, children=None, *args, **kw):
		self.children = children if children else list()
		super(NestedWidget, self).__init__(name_, title_, *args, **kw)

	def validate(self, data):
		for child in self.children:
			try:
				child.validate(data)
			except Exception as e:
				raise ValidationError(e)

	def _make_exception(self, valid, invalid, errors):
		return TransformException('', errors=errors, valid=valid, invalid=invalid)

	def _apply_native(self, widget, data):
		try:
			w_result = widget.native(data)
			if isinstance(w_result, (tuple, list)):
				w_result = w_result[0]
			w_errors = {}
		except TransformException as exc:
			w_result = exc.valid
			w_errors = exc
		except (ValueError, AttributeError, AssertionError) as exc:
			w_result = {widget.name: data.get(widget.name)}
			w_errors = TransformException('', valid=w_result, invalid={}, errors={widget._get_error_key(): exc})
		return w_result, w_errors

	def native(self, data):
		result = dict()
		errors = dict()
		
		for child in self.children:
			if isinstance(child, NestedWidget):
				ch_res, ch_err = self._apply_native(child, data)
				result.update(ch_res)
				if ch_err:
					ch_err = ch_err.errors or ch_err
					if isinstance(ch_err, dict):
						for key in ch_err.keys():
							if isinstance(ch_err[key], dict):
								inner = ch_err.pop(key)
								ch_err.update({'%s.%s' % (key, ikey): val for ikey, val in inner.iteritems()})
					errors[child._get_error_key()] = ch_err
				continue

			try:
				result[child.name] = child.native(data)
			except TransformException as error:
				errors[child._get_error_key()] = error.errors or error
			except (ValueError, AttributeError, AssertionError) as error:
					errors[child._get_error_key()] = error

		remaining = dict()
		
		for i in data:
			if i not in result:
				remaining[i] = data[i]

		if errors:
			raise self._make_exception(result, remaining, errors)

		return result, remaining


class Form(NestedWidget):
	def __init__(self, name_, title_=None, layout=None, children=[], footer=None, *args, **kw):
		super(Form, self).__init__(name_, title_, children, *args, **kw)
		
		self.layout = layout
		self.footer = footer
		
		if 'method' not in self.args:
			self.args['method'] = 'post'
	
	@property
	def template(self):
		return tag.form ( id = self.name + '-form', **self.args ) [
				([
					self.layout(self.name, children=self.children)(self.data)
				] if self.layout else [
					child(self.data) for child in self.children
				]) + ([
					self.footer(self.name)(self.data) if isinstance(self.footer, type) else self.footer(self.data)
				] if self.footer else [])
			]


class FieldSet(NestedWidget):
	def __init__(self, name_, title_=None, layout=None, children=[], *args, **kw):
		super(FieldSet, self).__init__(name_, title_, children, *args, **kw)
		
		self.layout = layout
	
	@property
	def template(self):
		return tag.fieldset (
				id = self.name + '-set',
				**self.args
			) [
				([tag.legend [ self.title ] ] if self.title else []) + ([
					self.layout(self.name, children=self.children)(self.data)
				] if self.layout else [
					child(self.data) for child in self.children
				])
			]


class Label(Widget):
	def __init__(self, name_, title_=None, for_=None, *args, **kw):
		self.for_ = for_
		super(Label, self).__init__(name_, title_, *args, **kw)
	
	@property
	def template(self):
		return tag.label (
				for_ = (self.for_.name + '-field') if self.for_ else None
			) [ self.title if self.title else self.for_.title ]


class Layout(NestedWidget):
	label = Label


class Input(Widget):
	type_ = None
	
	@property
	def template(self):
		return tag.input (
				type_ = self.type_,
				name = self.name,
				id = self.name + '-field',
				value = self.value,
				**self.args
			)

	def validate(self, data):
		super(Input, self).validate(data)
		value = data.get(self.name, None)
		if self.args.get('required', False):
			if not value or isinstance(value, str) and not value.strip():
				raise ValidationError('{} field is required.'.format(self.name))
		if self.args.get('pattern', False):
			pattern = re.compile("(?u)^" + self.args.get('pattern') + "$")
			if not pattern.match(value):
				raise ValidationError('{} field is invalid.'.format(self.name))


class BooleanInput(Input):
	transform = BooleanTransform()
	
	@property
	def template(self):
		return tag.div [[ tag.input (
					type_ = self.type_,
					name = self.name,
					id = self.name + '-field',
					checked = self.value,
					**self.args
				)] + [
					tag.label ( for_ = self.name + '-field' ) [ self.args.get('title') ]
				] if 'title' in self.args else []]


class Link(Widget):
	@property
	def template(self):
		return tag.a ( id = self.name + "-link", **self.args ) [ self.title ]
