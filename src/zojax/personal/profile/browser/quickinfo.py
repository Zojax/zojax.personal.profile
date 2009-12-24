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
from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds

from zojax.layoutform import Fields, PageletDisplayForm
from zojax.principal.profile.interfaces import IProfileFields
from zojax.principal.profile.interfaces import IPersonalProfile
from zojax.principal.profile.interfaces import IProfilesCategory
from zojax.personal.profile.interfaces import IProfileWorkspace

_marker = object()


class QuickInfo(PageletDisplayForm):

    @property
    def fields(self):
        content = self.content
        configlet = getUtility(IProfilesCategory)
        ids = getUtility(IIntIds)
        configletFields = configlet['default'].getFields()

        fields = []
        for id in configlet.quickInfoFields:
            field = ids.getObject(id)
            name = field.__name__
            if field in configletFields and field.visible:
                if content.get(name, field.missing_value) is not \
                        field.missing_value:
                    fields.append(field)

        return Fields(*fields)

    def update(self):
        context = self.context
        while not IProfileWorkspace.providedBy(context):
            context = context.__parent__

        self.workspace = context
        self.profile = IPersonalProfile(context.__principal__)
        self.content = self.profile.getProfileData()

        self.timezone = self.profile.timezone
        self.registered = self.profile.registered
        self.lastLoginTime = self.profile.lastLoginTime

        super(QuickInfo, self).update()

    def getContent(self):
        return self.content
