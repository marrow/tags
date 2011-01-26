# encoding: utf-8

from marrow.widgets import *


search = Form('site-search', action='/search', method='get', children=[
        SearchField('q', autofocus=True, autocomplete="on", placeholder="Site-wide search.")
    ])
