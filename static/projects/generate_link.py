#! /usr/bin/env python
import sys, hashlib

if len(sys.argv) != 2:
	print 'USAGE: ' + sys.argv[0] + ' <dir_name>'
	sys.exit(0)

d = sys.argv[1].strip('/')
print 'http://exstudio.ro/default/access/' + hashlib.sha1(d).hexdigest()