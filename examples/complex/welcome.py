#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals

from marrow.tags.html5 import *

from master import SITE_NAME, site_header, site_footer


def welcome():
    return html [
            head [ title [ 'Welcome!', ' — ', SITE_NAME ] ],
            flush, # allow the browser to start downloading static resources early
            body ( class_ = "nav-welcome" ) [
                    site_header(),
                    p [
                            'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
                        ],
                    site_footer()
                ]
        ]


if __name__ == '__main__':
    with open('welcome.html', 'w') as fh:
        for i in welcome().render('utf8'):
            fh.write(i)
