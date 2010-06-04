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
from zope import interface
from zope.component import getUtility, getMultiAdapter
from zope.app.intid.interfaces import IIntIds

from z3c.form.group import Group
from z3c.form.interfaces import DISPLAY_MODE, IDisplayForm

from zojax.layout.interfaces import IPagelet
from zojax.layoutform import Fields, PageletDisplayForm
from zojax.content.type.interfaces import IOrder
from zojax.principal.profile.interfaces import IProfilesCategory
from zojax.principal.profile.interfaces import IPrincipalInformation
from zojax.principal.profile.interfaces import IProfileFields, IPersonalProfile

_marker = object()


class ProfileView(PageletDisplayForm):

    mode = DISPLAY_MODE

    def getContent(self):
        return self.profile.getProfileData()

    def updateForms(self):
        super(ProfileView, self).updateForms()
        ids = getUtility(IIntIds)
        fields = getUtility(IProfileFields).getFields()

        content = self.profile.getProfileData()
        category = getUtility(IProfilesCategory)
        quickInfo = category.quickInfoFields
        fieldCategories = category.fieldCategories

        default = []
        categories = {}
        for field in fields:
            name = field.__name__
            if not field.visible or ids.getId(field) in quickInfo:
                continue

            value = content.get(name, field.missing_value)
            if value is field.missing_value or value is None:
                continue

            if field.category not in fieldCategories:
                default.append(field)
            else:
                categories.setdefault(field.category, []).append(field)

        self.groups = list(self.groups)

        if default:
            group = Category(self.context, self.request, self, u'', default)
            group.update()
            self.groups.append(group)

        for key in fieldCategories:
            if key not in categories:
                continue
            fields = categories[key]
            if fields:
                group = Category(self.context, self.request, self, key, fields)
                group.update()
                self.groups.append(group)

    def update(self):
        self.profile = IPersonalProfile(self.context.__principal__)
        self.title = self.profile.title
        self.photoUrl = self.profile.photoUrl(self.request)

        super(ProfileView, self).update()


class Category(Group):
    interface.implements(IDisplayForm)

    mode = DISPLAY_MODE

    def __init__(self, context, request, form, label, fields):
        super(Category, self).__init__(context, request, form)

        self.label = label
        self.fields = Fields(*fields)

    def getContent(self):
        return self.parentForm.getContent()

    def postUpdate(self):
        pass
