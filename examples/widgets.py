# encoding: utf-8

from __future__ import unicode_literals

from timeit import Timer

from marrow.tags import html5 as tag

from marrow.widgets import *



if __name__ == '__main__':
    search = Form('site-search', action='/search', method='get', children=[
            SearchField('q', autofocus=True, autocomplete="on", placeholder="Site-wide search.")
        ])

    login = Form('sign-in', class_="tabbed", action='/users/action:authenticate', children=[
            HiddenField('referrer'),
            FieldSet('local', "Local Users", TableLayout, [
                    TextField('identity', "User Name"),
                    PasswordField('password', "Password")
                ]),
            FieldSet('openid', "OpenID Users", TableLayout, [
                    URLField('url', "OpenID URL")
                ])
        ], footer=SubmitFooter('form', "Sign In"))


    contact = Form('contact', action="/contact", children=[
            FieldSet('contact', "Send us a Message", DefinitionListLayout, [
                    TextField('name', "Your Name", required=True, autofocus=True),
                    EmailField('email', "Your E-Mail Address", required=True),
                    PhoneField('phone', "Your Phone Number"),
                    TextArea('details', "Details")
                ])
        ], footer=SubmitFooter('form', "Send Message"))

    select = SelectField('myselect', values=[
            (None, 'Default Template'),
            ("Custom Templates", [
                    ('home', "Homepage"),
                    ('contact', "Contact Form")
                ])
        ])

    select2 = SelectField('select2', size=10, values=[
            (None, 'Default Template'),
            ("Custom Templates", [
                    ('home', "Homepage"),
                    ('contact', "Contact Form")
                ])
        ])

    page = tag.html [
            tag.head [
                    tag.meta ( charset = "utf-8" ),
                    tag.title [ "Example Widgets" ]
                ],
            
            "\n",
            
            tag.body [
                    tag.h1 [ "Example Widgets" ],
                    "\n\n",
                
                    tag.h2 [ "Search" ],
                    "\n",
                    search(),
                    "\n\n",
                
                    tag.h2 [ "Login" ],
                    "\n",
                    login(),
                    "\n\n",
                
                    tag.h2 [ "Contact" ],
                    "\n",
                    contact(),
                    "\n\n",
                
                    tag.h2 [ "Select Fields" ],
                    "\n\n",
                
                    tag.h3 [ "Raw Select" ],
                    "\n",
                    select(),
                    "\n\n",
                
                    tag.h3 [ "Raw Select w/ Data" ],
                    "\n",
                    select({'myselect': 'home'}),
                    "\n\n",
                
                    tag.h3 [ "Raw Select, Large" ],
                    "\n",
                    select2(),
                    "\n",
                ]
        ]
    
    print unicode(page)
    
    n = 5000
    duration = Timer("list(page.render())", "from __main__ import page").timeit(n)
    timeper = duration / float(n) * 1000
    genper = float(n) / duration
    print "Timeit (Widget Stream): %0.2fs for %d gens: %0.2f usec/gen (%d gen/sec)." % (duration, n, timeper, genper)
    
    duration = Timer("unicode(page)", "from __main__ import page").timeit(n)
    timeper = duration / float(n) * 1000
    genper = float(n) / duration
    print "Timeit (Widget Monolithic): %0.2fs for %d gens: %0.2f usec/gen (%d gen/sec)." % (duration, n, timeper, genper)
