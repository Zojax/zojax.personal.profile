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
""" zojax.workspace.manager tests

$Id$
"""
import os, unittest, doctest
from persistent import Persistent
from zope import interface, component
from zope.app.rotterdam import Rotterdam
from zojax.filefield.testing import ZCMLLayer, FunctionalDocFileSuite
from zojax.layoutform.interfaces import ILayoutFormLayer
from zojax.principal.field.interfaces import IUser
from zojax.content.type.interfaces import ISearchableContent

zojaxPersonalProfileLayer = ZCMLLayer(
    os.path.join(os.path.split(__file__)[0], 'ftesting.zcml'),
    __name__, 'zojaxPersonalProfileLayer', allow_teardown=True)


class PrincipalInformation(object):

    readonly = True
    firstname = u''
    lastname = u''
    email = u'user@zojax.net'

    def __init__(self, principal):
        self.principal = principal

    @property
    def title(self):
        return self.principal.title


class Principal(Persistent):
    interface.implements(IUser, ISearchableContent)
         
    def __init__(self, id, title):
        self.id = id
        self.title = title


class IDefaultSkin(ILayoutFormLayer, Rotterdam):
    """ skin """


def test_suite():
    testbrowser = FunctionalDocFileSuite(
        "testbrowser.txt",
        optionflags=doctest.ELLIPSIS|doctest.NORMALIZE_WHITESPACE)
    testbrowser.layer = zojaxPersonalProfileLayer

    return unittest.TestSuite((testbrowser, ))
