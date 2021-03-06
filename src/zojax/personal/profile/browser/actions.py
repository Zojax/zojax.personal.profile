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
from zope.security import checkPermission
from zope.component import queryMultiAdapter
from zope.app.pagetemplate import ViewPageTemplateFile

from zojax.preferences.utils import hasEditableFields
from zojax.preferences.interfaces import IRootPreferences
from zojax.preferences.interfaces import IPreferenceGroup
from zojax.preferences.interfaces import IPreferenceCategory


class ProfileActions(object):

    data = None
    template = ViewPageTemplateFile('actions.pt')

    def isAvailable(self):
        return self.data is not None

    def update(self):
        super(ProfileActions, self).update()

        context = self.context
        if not checkPermission('zojax.ModifyPreference', context):
            return

        path = []
        parent = context
        while IPreferenceGroup.providedBy(parent):
            path.insert(0, parent)
            parent = parent.__parent__

        self.root, path = path[0], path[1:]
        if not path:
            path = [self.root]

        self.data = self._process(self.root, path)

    def _process(self, context, path, level=1):
        request = self.request
        maincontext = self.context

        if path:
            data = []
            items = getattr(context, 'items', ())
            if callable(items):
                items = items()

            for name, prefs in items:
                if not prefs.isAvailable():
                    continue

                info = {'name': name,
                        'title': prefs.__title__,
                        'icon': queryMultiAdapter(
                                       (prefs, request), name='zmi_icon'),
                        'items': (),
                        'selected': False,
                        'prefs': prefs,
                        'level': level,
                        'editable': True}

                if prefs.__id__ == path[0].__id__:
                    info['items'] = self._process(prefs, path[1:], level+1)
                elif prefs.__parent__.__id__ == '':
                    info['items'] = self._process(prefs, [self.root], level+1)
                    if len(info['items']) == 1:
                        info['items'] = ()

                if prefs.__id__ == self.context.__id__:
                    info['selected'] = True

                if IPreferenceCategory.providedBy(prefs):
                    if not info['items']:
                        if not self._process(prefs, [prefs], level+1) \
                                and not hasEditableFields(prefs):
                            continue
                    elif not hasEditableFields(prefs):
                        info['editable'] = False

                data.append(info)

            return data
