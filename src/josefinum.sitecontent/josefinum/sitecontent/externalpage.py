from five import grok
from Acquisition import aq_inner, aq_parent
from plone.directives import dexterity, form

from zope import schema
from zope.component import getMultiAdapter

from plone.namedfile.interfaces import IImageScaleTraversable

from josefinum.sitecontent import MessageFactory as _


class IExternalPage(form.Schema, IImageScaleTraversable):
    """
    A page rendering linked content in an iframe
    """
    remote_url = schema.URI(
        title=_(u"Remote URI"),
        description=_(u"Please enter complete URI to external location"),
        required=True,
    )
    width = schema.TextLine(
        title=_(u"iFrame Width"),
        description=_(u"Provide a width for the iframe window. If the "
                      u"external site is larger a scrollbar will appear"),
        required=False,
    )
    height = schema.TextLine(
        title=_(u"iFrame Height"),
        description=_(u"Set a height for the iframe window"),
        required=False,
    )


class ExternalPage(dexterity.Item):
    grok.implements(IExternalPage)


class View(grok.View):
    grok.context(IExternalPage)
    grok.require('zope2.View')
    grok.name('view')

    def update(self):
        self.parent_url = self.parent_link()

    def parent_link(self):
        context = aq_inner(self.context)
        context_helper = getMultiAdapter((context, self.request),
                                         name="plone_context_state")
        canonical = context_helper.canonical_object()
        parent = aq_parent(canonical)
        return parent.absolute_url()
