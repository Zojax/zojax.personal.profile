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
from zope.location import Location
from zope.component import getUtility
from zojax.preferences.interfaces import IPreferenceGroup
from zojax.personal.space.interfaces import IPersonalSpace
from zojax.personal.space.interfaces import IPersonalWorkspaceDescription
from zojax.content.actions.interfaces import IDoNotCacheActionsPortlet

from interfaces import _, IProfileWorkspace, IProfileWorkspaceFactory


class ProfileWorkspaceFactory(object):
    component.adapts(IPersonalSpace)
    interface.implements(IProfileWorkspaceFactory)

    name = 'profile'
    title = _(u'Personal Profile')
    description = u''
    weight = 1

    def __init__(self, space):
        self.space = space

    def get(self):
        root = getUtility(IPreferenceGroup)
        root = root.__bind__(self.space.principal, self.space)
        root.__name__ = u'profile'
        root.__title__ = _(u'Profile')
        root.__description__ = u''

        interface.alsoProvides(
            root, IProfileWorkspace, IDoNotCacheActionsPortlet)
        return root

    install = get

    def uninstall(self):
        pass

    def isInstalled(self):
        return False

    def isAvailable(self):
        return True


class ProfileWorkspaceDescription(object):
    interface.implements(IPersonalWorkspaceDescription)

    name = 'profile'
    title = _(u'Profile')
    description = u''

    def createTemp(self, context):
        root = getUtility(IPreferenceGroup)
        clone = root.__class__.__new__(root.__class__)
        clone.__dict__.update(root.__dict__)

        clone.__name__ = u'profile'
        clone.__title__ = _(u'Profile')
        clone.__description__ = u''
        clone.__parent__ = context

        interface.alsoProvides(clone, IProfileWorkspace)
        return clone
