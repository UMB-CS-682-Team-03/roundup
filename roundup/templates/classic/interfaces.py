# $Id: interfaces.py,v 1.4 2001-07-30 01:25:57 richard Exp $

import urlparse, os

import instance_config
from roundup import cgi_client, mailgw 

class Client(cgi_client.Client): 
    ''' derives basic mail gateway implementation from the standard module, 
        with any specific extensions 
    ''' 
    TEMPLATES = instance_config.TEMPLATES

class MailGW(mailgw.MailGW): 
    ''' derives basic mail gateway implementation from the standard module, 
        with any specific extensions 
    ''' 
    ISSUE_TRACKER_EMAIL = instance_config.ISSUE_TRACKER_EMAIL
    ADMIN_EMAIL = instance_config.ADMIN_EMAIL
    MAILHOST = instance_config.MAILHOST

#
# $Log: not supported by cvs2svn $
# Revision 1.3  2001/07/29 07:01:39  richard
# Added vim command to all source so that we don't get no steenkin' tabs :)
#
# Revision 1.2  2001/07/29 04:07:37  richard
# Fixed the classic template so it's more like the "advertised" Roundup
# template.
#
# Revision 1.1  2001/07/23 23:28:43  richard
# Adding the classic template
#
# Revision 1.1  2001/07/23 23:16:01  richard
# Split off the interfaces (CGI, mailgw) into a separate file from the DB stuff.
#
#
# vim: set filetype=python ts=4 sw=4 et si
