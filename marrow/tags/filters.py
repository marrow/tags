# TODO: This is just an idea at the moment.
# See:
#  http://code.activestate.com/recipes/276960/
#  http://code.activestate.com/recipes/576756/
#  http://code.activestate.com/recipes/576757/

__all__ = ['Filter']


class Filter(object):
	def __init__(self):
		self._input = None
	
	def __ror__(self, left):
		self._input = left
	
	def __call__(self, context):
		return self._input(context)

