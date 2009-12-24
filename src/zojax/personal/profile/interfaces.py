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
""" zojax.workspace.profile interfaces

$Id$
"""
from zope import schema, interface
from zope.i18nmessageid import MessageFactory
from zojax.content.space.interfaces import IWorkspace, IWorkspaceFactory
from zojax.content.notifications.interfaces import IContentNotification

_ = MessageFactory('zojax.personal.profile')


class IProfileWorkspace(IWorkspace):
    """ profile workspace """


class IProfileWorkspaceFactory(IWorkspaceFactory):
    """ profile workspace factory """


class IRegistrationNotification(IContentNotification):
    """ email registration """


class IPrincipalRegisteredActivityRecord(interface.Interface):
    """ principal registered activity record """
