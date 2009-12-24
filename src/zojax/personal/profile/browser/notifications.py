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
from zope.component import getUtility
from zope.app.component.hooks import getSite
from zope.app.security.interfaces import IAuthentication, PrincipalLookupError

from zojax.layoutform import button, Fields
from zojax.layoutform.interfaces import ISaveAction
from zojax.wizard.step import WizardStepForm
from zojax.statusmessage.interfaces import IStatusMessage
from zojax.principal.field import UserField
from zojax.principal.profile.interfaces import IPersonalProfile
from zojax.principal.registration.interfaces import _
from zojax.personal.profile.notifications import RegistrationNotification


class INotificationsForm(interface.Interface):

    principal = UserField(
        title = _(u'User'),
        description = _('Select user for notifications.'),
        required = False)


class NotificationsForm(WizardStepForm):

    fields = Fields(INotificationsForm)
    ignoreContext = True

    def update(self):
        self.notification = RegistrationNotification(getSite())

        super(NotificationsForm, self).update()

        request = self.request

        if 'form.unsubscribe' in request:
            principals = request.get('form.principals', ())
            for pid in principals:
                self.notification.unsubscribe(pid)

            if principals:
                IStatusMessage(request).add(
                    _('Selected users have been unsubscribed.'))

        principals = []
        auth = getUtility(IAuthentication)

        for pid in self.notification.getSubscribers(getSite()):
            try:
                principal = auth.getPrincipal(pid)
            except PrincipalLookupError:
                continue

            profile = IPersonalProfile(principal)
            principals.append(
                (profile.title, {'id': pid, 'title': profile.title}))

        principals.sort()
        self.principals = [info for _t, info in principals]

    @button.buttonAndHandler(_(u'Select'), name="select", provides=ISaveAction)
    def selectButtonHandler(self, action):
        data, errors = self.extractData()
        if not data['principal']:
            IStatusMessage(self.request).add(
                _('Please select user.'), 'warning')
        else:
            self.notification.subscribe(data['principal'])
            IStatusMessage(self.request).add(_('User has been subscribed.'))
            self.redirect('.')
