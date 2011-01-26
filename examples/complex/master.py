# encoding: utf-8

from __future__ import unicode_literals

from marrow.tags.html5 import *
from widgets import search

from datetime import datetime


SITE_NAME = "Contentment, the WebCore CMS"


def site_header():
    return div ( strip = True ) [
            header [
                    hgroup [
                            h1 [ "Contentment" ],
                            h2 [ "The most awesome CMS in the world!" ]
                        ],
                    aside ( class_ = "fr" ) [ search() ]
                ],
            flush
        ]


def site_footer():
    return footer [
            p [
                    "Copyright © 2010-",
                    datetime.utcnow().year,
                    " Alice Bevan-McGregor"
                ]
        ]
