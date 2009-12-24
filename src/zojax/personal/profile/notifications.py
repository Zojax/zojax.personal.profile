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
from zope import interface, component
from zope.app.component.hooks import getSite
from zope.app.component.interfaces import ISite
from zojax.subscription.interfaces import ISubscriptionDescription
from zojax.content.notifications.utils import sendNotification
from zojax.content.notifications.notification import Notification
from zojax.principal.registration.interfaces import IPrincipalRegisteredEvent

from interfaces import _, IRegistrationNotification


class RegistrationNotification(Notification):
    component.adapts(ISite)
    interface.implementsOnly(IRegistrationNotification)

    type = u'registration'
    title = _(u'Registration')
    description = _(u'User registrations notifications.')


class RegistrationNotificationDescription(object):
    interface.implements(ISubscriptionDescription)

    title = _(u'Registration')
    description = _(u'User registrations notifications.')


@component.adapter(IPrincipalRegisteredEvent)
def principalRegisteredHandler(ev):
    sendNotification('registration', getSite(), ev)
