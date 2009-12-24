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
from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds, IIntIdAddedEvent
from zope.app.component.hooks import getSite

from zojax.activity.record import ActivityRecord
from zojax.activity.interfaces import IActivity, IActivityRecordDescription
from zojax.content.activity.interfaces import IContentActivityRecord
from zojax.authentication.interfaces import IPrincipalRemovingEvent
from zojax.principal.registration.interfaces import IPrincipalRegisteredEvent

from interfaces import _, IPrincipalRegisteredActivityRecord


class PrincipalRegisteredActivityRecord(ActivityRecord):
    interface.implements(IPrincipalRegisteredActivityRecord,
                         IContentActivityRecord)

    type = u'registration'
    verb = _('joined site')


class PrincipalRegisteredActivityRecordDescription(object):
    interface.implements(IActivityRecordDescription)

    title = _(u'Principal registration')
    description = _(u'New principal has been registered.')


@component.adapter(IPrincipalRegisteredEvent)
def principalRegisteredHandler(event):
    principal = event.principal
    getUtility(IActivity).add(
        getSite(),
        PrincipalRegisteredActivityRecord(principal = event.principal.id))


@component.adapter(IPrincipalRemovingEvent)
def principalRemovingHandler(event):
    activity = getUtility(IActivity)
    for record in activity.search(
        type = {'any_of': (u'registration',)},
        principal = {'any_of': (event.principal.id,)}):
        activity.remove(record.id)
