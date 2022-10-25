from datetime import datetime

import marrow.tags

from html.tag import div, header, hgroup, h1, h2, aside, footer, p

from widgets import search



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
        ]


def site_footer():
    return footer [
            p [
                    "Copyright © 2010-",
                    datetime.utcnow().year,
                    " Alice Bevan-McGregor"
                ]
        ]
