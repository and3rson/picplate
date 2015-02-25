#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from ticket import Ticket

t = Ticket(filename='file.xml', width=900, height=900)
t.assign(title='Some activity', date='Some date', club='Wherever', address=1)
img = t.render()
img.save('out.png')
