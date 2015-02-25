#!/usr/bin/env python2

from ticket import Ticket

t = Ticket(filename='file.xml', width=900, height=900)
t.assign(title='Some activity', date='Some date', club='Wherever', address='Somewhere')
img = t.render()
img.save('out.png')