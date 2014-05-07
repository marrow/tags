# encoding: utf-8

from __future__ import unicode_literals
from marrow.widgets.base import ValidationError, Form
import unittest
from marrow.widgets import Input


class TestValidation(unittest.TestCase):
    def setUp(self):
        super(TestValidation, self).setUp()

    def test_required_fail(self):
        test_input = Input(type_='text', name_='test', required=True)
        with self.assertRaisesRegexp(ValidationError, 'field is required.'):
            test_input.validate({'test': ''})

    def test_required_success(self):
        test_input = Input(type_='text', name_='test', required=True)
        try:
            test_input.validate({'test': 'test data'})
        except ValidationError as e:
            self.fail(e)

    def test_regex_fail(self):
        test_input = Input(type_='text', name_='test', pattern=r'\w+')
        with self.assertRaisesRegexp(ValidationError, 'field is invalid.'):
            test_input.validate({'test': 'abcABC123!'})

    def test_regex_success(self):
        test_input = Input(type_='text', name_='test', pattern=r'\w+')
        try:
            test_input.validate({'test': 'abcéèàùçœëüABC12ÉÈÀÙÇŒEËAÄ'})
        except ValidationError as e:
            self.fail(e)

    def test_nested(self):
        nested_widget = Form(name_='test', children=[
            Input(type_='text', name_='test_pattern', pattern=r'\w+'),
            Input(type_='text', name_='test_required', required=True),
        ])
        try:
            nested_widget.validate({
                'test_pattern': 'abcABC123',
                'test_required': 'required_data'
            })
        except ValidationError as e:
            self.fail(e)
