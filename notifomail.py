#!/usr/local/bin/python

# NotifoMail:
# A Python script to process piped e-mails and post a Notifo alert,
# for use with e-mail forwarders such as Exim.
#
# Requires the following Python modules:
#   Notifo.py
#       <http://github.com/mrtazz/notifo.py>
#   Python 2.6 or SimpleJSON
#       <http://pypi.python.org/pypi/simplejson/>
#
# Released under the BSD License; see file LICENSE for information.
#
# Be sure to enter your username and API key in notifomail.cfg
# before running this script - otherwise it won't work.
#
# Cody "codeman38" Boisclair
# 3 September 2010


import sys, os, ConfigParser
from notifo import Notifo

# Read the config file.
config = ConfigParser.ConfigParser()
config.read(['notifomail.cfg', \
            os.path.abspath(os.path.dirname(sys.argv[0]))+'/notifomail.cfg'])

# Check to make sure we've got a username and key.
# If we don't have one, quit.
# Don't display a message or anything, because Exim will bounce.
if not config.has_option('Login', 'user') or \
   config.get('Login', 'user') == '' or \
   not config.has_option('Login', 'secret') or \
   config.get('Login', 'secret') == '':
    sys.stderr.write('No username or API secret specified!\n')
    sys.exit(1)
	
if not config.has_option('Format', 'title'):
    config.set('Format', 'title', 'New E-mail')
if not config.has_option('Format', 'label'):
    config.set('Format', 'label', 'NotifoMail')
if not config.has_option('Format', 'lines'):
    config.set('Format', 'lines', '5')

# Read the e-mail, find the Subject and From lines,
# and read the first several lines of the body.
body = ''
try:
	while True:
		line = raw_input()
		if line.startswith('From: '):
			sender = line[6:]
		if line.startswith('Subject: '):
			subject = line[9:]
		if line == '':
			break

	num_lines = 0
	while num_lines < config.getint('Format','lines'):
		line = raw_input()
		body += line + "\n"
		num_lines += 1
except EOFError:
	pass

msg = 'Subject: %s\nFrom: %s' % (subject, sender)
if body != '':
	msg += '\n\n' + body + '...'

if subject != '' and sender != '':
	notifo = Notifo(config.get('Login','user'), config.get('Login','secret'))
	notifo.send_notification(label=config.get('Format','label'), \
                             title=config.get('Format','title'), msg=msg)
