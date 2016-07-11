#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id$"
#end_pymotw_header

import dns.resolver
import email.utils
from email.mime.text import MIMEText

from network_programming import smtplib

# Create the message
msg = MIMEText('This is the body of the message.')
msg['To'] = email.utils.formataddr(('Recipient',
                                    'socialpercon@gmail.com'))
msg['From'] = email.utils.formataddr(('Author',
                                      'socialpercon@mobigen.com'))
msg['Subject'] = 'Simple test message'

answers = dns.resolver.query('mobigen.com', 'MX')
print str(answers[0].exchange)

server = smtplib.SMTP(str(answers[0].exchange))
server.set_debuglevel(True) # show communication with the server
try:
    server.sendmail('socialpercon@gmail.com',
                    ['socialpercon@mobigen.com'],
                    msg.as_string())
finally:
    server.quit()
