# encoding: utf-8

# TODO: This is just an idea at the moment.

__all__ = ['Filter']


class Filter(object):
    def __init__(self):
        self._input = None
    
    def __ror__(self, left):
        self._input = left
    
    def __call__(self, context):
        return self._input(context)
    