from Acquisition import aq_inner
from AccessControl import Unauthorized

from five import grok
from plone import api

from z3c.form import group, field
from zope import schema
from zope.component import getMultiAdapter

from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Container

from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable

from plone.keyring import django_random
from Products.CMFPlone.utils import safe_unicode

from kk.sitecontent.contentmodule import IContentModule

from kk.sitecontent import MessageFactory as _


class IContentPage(form.Schema, IImageScaleTraversable):
    """
    Folderish contentpage containing submodules
    """
    headline = schema.TextLine(
        title=_(u"Headline"),
        description=_(u"Override the actual title with a content headline in"
                      u"order to keep the dublin core metadata short and "
                      u"precise"),
        required=False
    )
    text = RichText(
        title=_(u"Body Text"),
        required=False
    )


class ContentPage(Container):
    grok.implements(IContentPage)
    pass


class View(grok.View):
    grok.context(IContentPage)
    grok.require('zope2.View')
    grok.name('view')

    def updates(self):
        self.has_submodules = len(self.contained_modules()) > 0

    def rendered_contentmodule(self, item):
        context = item.getObject()
        tmpl = context.restrictedTraverse('@@content-view')()
        return tmpl

    def contained_modules(self):
        context = aq_inner(self.context)
        catalog = api.portal.get_tool(name='portal_catalog')
        items = catalog(object_provides=IContentModule.__identifier__,
                        path=dict(query='/'.join(context.getPhysicalPath()),
                                  depth=1),
                        sort_on='getObjPositionInParent')
        return items

    def can_edit(self):
        return not api.user.is_anonymous()


class ManageModules(grok.View):
    grok.context(IContentPage)
    grok.require('cmf.ModifyPortalContent')
    grok.name('manage-modules')

    def update(self):
        context = aq_inner(self.context)
        self.has_subcontent = len(self.contained_modules()) > 0
        self.errors = {}
        unwanted = ('_authenticator', 'form.button.Submit')
        required = ('title')
        if 'form.button.Submit' in self.request:
            authenticator = getMultiAdapter((context, self.request),
                                            name=u"authenticator")
            if not authenticator.verify():
                raise Unauthorized
            form = self.request.form
            form_data = {}
            form_errors = {}
            errorIdx = 0
            for value in form:
                if value not in unwanted:
                    form_data[value] = safe_unicode(form[value])
                    if not form[value] and value in required:
                        error = {}
                        error['active'] = True
                        error['msg'] = _(u"This field is required")
                        form_errors[value] = error
                        errorIdx += 1
                    else:
                        error = {}
                        error['active'] = False
                        error['msg'] = form[value]
                        form_errors[value] = error
            if errorIdx > 0:
                self.errors = form_errors
            else:
                self._create_subcontent(form)

    def _create_subcontent(self, data):
        context = aq_inner(self.context)
        new_title = data['title']
        token = django_random.get_random_string(length=18)
        api.content.create(
            type='kk.sitecontent.contentmodule',
            id=token,
            title=new_title,
            container=context,
            safe_id=True
        )
        url = context.absolute_url()
        return self.request.response.redirect(url)

    def contained_modules(self):
        context = aq_inner(self.context)
        catalog = api.portal.get_tool(name='portal_catalog')
        items = catalog(object_provides=IContentModule.__identifier__,
                        path=dict(query='/'.join(context.getPhysicalPath()),
                                  depth=1),
                        sort_on='getObjPositionInParent')
        return items

    def item_state_klass(self, uid):
        klass = 'acm-item-default'
        if not api.user.is_anonymous():
            state = self.item_state_info(uid=uid)
            klass = ('acm-item--{0}').format(state)
        return klass

    def item_state_info(self, uid):
        item = api.content.get(UID=uid)
        state = api.content.get_state(obj=item)
        return state
