#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals

from collections import namedtuple

from marrow.tags.html5 import *

from master import SITE_NAME, site_header, site_footer



def developers(devs):
    return html [
            head [ title [ 'Developers and Contributors', ' — ', SITE_NAME ] ],
            flush, # allow the browser to start downloading static resources early
            body ( class_ = "nav-developers" ) [
                    site_header(),
                    
                    h1 [ "Our Beloved Developers" ],
                    p ( class_ = "heart-attack" ) [
                            'Developers developers developers developers.  Developers.  Developers.  Developers.  Developers.  Developers!  Developers!  Developers!  Developers!  DEVELOPERS!  DEVELOPERS!  DEVELOPERS!  DEVELOPERS!'
                        ],
                    
                    table [
                            thead [
                                    th [ "Name" ],
                                    th [ "Position" ],
                                    th [ "E-Mail Address" ]
                                ],
                            
                            tbody [[
                                    tr [
                                            td [ developer.name ],
                                            td [ developer.position ],
                                            td [ developer.email ],
                                        ] for developer in devs
                                ]]
                        ],
                    
                    site_footer()
                ]
        ]


if __name__ == '__main__':
    Developer = namedtuple('Developer', ('name', 'position', 'email'))
    
    DEVELOPERS = [
            Developer("Alice Bevan-McGregor", "Chief Architect", "alice@..."),
            Developer("Alex Grönholm", "Core Developer", "alex@..."),
            Developer("Howard Bevan", "Fellow", "hbevan@..."),
            Developer("Chimps, the Monkey", "Mascot", "chimps@...")
        ]
    
    with open('developers.html', 'w') as fh:
        for i in developers(DEVELOPERS).render('utf8'):
            fh.write(i)
