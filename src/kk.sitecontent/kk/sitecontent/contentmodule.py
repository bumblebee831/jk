from five import grok

from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Container

from plone.directives import form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedBlobImage
from plone.namedfile.interfaces import IImageScaleTraversable

from kk.sitecontent import MessageFactory as _


moduleklass = SimpleVocabulary(
    [SimpleTerm(value=u'module-kkj', title=_(u'KKJ')),
     SimpleTerm(value=u'module-fk', title=_(u'FK')),
     SimpleTerm(value=u'module-kjpp', title=_(u'KJPP')),
     SimpleTerm(value=u'module-jsf', title=_(u'Josefinum'))]
)


class IContentModule(form.Schema, IImageScaleTraversable):
    """
    A single module addable to content pages
    """ 
    image = NamedBlobImage(
        title=_(u"Image"),
        required=False,
    )
    text = RichText(
        title=_(u"Body Text"),
        required=False,
    )
    moduleklass = schema.Choice(
        title=_(u"Module CSS Class Selection"),
        vocabulary=moduleklass,
        required=False,
    )


class ContentModule(Container):
    grok.implements(IContentModule)
    pass


class View(grok.View):
    grok.context(IContentModule)
    grok.require('zope2.View')
    grok.name('view')


class ContentView(grok.View):
    grok.context(IContentModule)
    grok.require('zope2.View')
    grok.name('content-view')
