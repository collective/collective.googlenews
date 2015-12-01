# coding: utf-8
from collective.googlenews import _
from collective.googlenews.utils import _valid_as_standout_journalism
from plone.directives import form
from plone.supermodel import model
from zope import schema
from zope.interface import Invalid
from zope.interface import invariant
from zope.interface import provider


@provider(form.IFormFieldProvider)
class IGoogleNews(model.Schema):

    """Behavior interface to add some Google News features."""

    model.fieldset(
        'google-news',
        label=_(u'Google News'),
        fields=['standout_journalism', 'news_keywords'],
    )

    # https://support.google.com/news/publisher/answer/191283
    standout_journalism = schema.Bool(
        title=_(u'Standout Journalism'),
        description=_(
            u'help_standout_journalism',
            default=u'Used to indicate this is a big story, or an extraordinary work of journalism. '
                    u'You can mark as standout no more than seven news articles in the past calendar week. '
                    u'Implements Google News <code>standout</code> metatag.',
        ),
        required=False,
    )

    # https://support.google.com/news/publisher/answer/68297
    news_keywords = schema.Tuple(
        title=_(u'Keywords'),
        description=_(
            u'help_news_keywords',
            default=u'Used to specify keywords that are relevant to this news article. '
                    u'Add one phrase or keyword on each line. '
                    u'Implements Google News <code>news_keywords</code> metatag.',
        ),
        value_type=schema.TextLine(),
        required=False,
    )

    @invariant
    def validate_standout_journalism(data):
        context = data.__context__  # this will be None when adding
        if not _valid_as_standout_journalism(context):
            raise Invalid(_(
                u"Can't mark this news article as standout. "
                u'There are already seven marked in the past calendar week.'
            ))
