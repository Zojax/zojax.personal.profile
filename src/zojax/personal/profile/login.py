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
import datetime
from zope import interface, component
from zope.datetime import parseDatetimetz
from zope.traversing.browser import absoluteURL
from zope.security.interfaces import IPrincipal
from zope.security import checkPermission
from zope.app.component.hooks import getSite
from zojax.statusmessage.interfaces import IStatusMessage
from zojax.principal.profile.interfaces import IPersonalProfile
from zojax.authentication.interfaces import ISuccessLoginAction

from interfaces import _


class SuccessLoginAction(object):
    interface.implements(ISuccessLoginAction)
    component.adapts(IPrincipal, interface.Interface)

    order = 100

    def __init__(self, principal, request):
        self.principal = principal
        self.request = request

    def __call__(self, nextURL):
        profile = IPersonalProfile(self.principal)

        if not profile.isComplete() and checkPermission('zojax.PersonalSpace', getSite()):
            if profile.firstname and profile.lastname:
                profile.modified = parseDatetimetz(str(datetime.datetime.now()))

            space = profile.space
            if space is not None:
                self.request.response.redirect(
                    u'%s/profile/profile/'%absoluteURL(space, self.request))

                IStatusMessage(self.request).add(
                    _('You successfully logged in to portal. Please complete your profile.'))

                return True

        return False
