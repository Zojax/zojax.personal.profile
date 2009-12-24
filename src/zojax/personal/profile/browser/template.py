##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
from datetime import datetime
from email.Utils import formataddr

from zope.component import getUtility
from zope.traversing.browser import absoluteURL
from zope.app.component.hooks import getSite
from zope.app.intid.interfaces import IIntIds

from zojax.ownership.interfaces import IOwnership
from zojax.principal.profile.interfaces import IPersonalProfile


class NotificationMail(object):

    space = u''

    def update(self):
        request = self.request
        principal = self.contexts[0].principal
        self.principal = principal
        self.profile = IPersonalProfile(principal)

        profile = IPersonalProfile(principal)
        if profile.email:
            author = profile.title
            self.author = author
            self.addHeader(u'From', formataddr((author, profile.email),))
            self.addHeader(u'To', formataddr((self.author, profile.email),))
        else:
            self.author = principal.title or principal.id

        if profile.space is not None:
            self.space = u'%s/'%absoluteURL(profile.space, request)

        self.email = profile.email
        self.messageId = u'<%s@zojax.net>'%principal.id
        self.now = datetime.now()

    @property
    def subject(self):
        return u'New principal has been registered: %s'%self.principal.title
