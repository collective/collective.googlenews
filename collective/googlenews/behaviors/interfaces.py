# coding: utf-8
from collective.googlenews import _
from collective.googlenews.utils import get_current_standout_journalism
from plone import api
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import Invalid
from zope.interface import invariant
from zope.interface import provider


@provider(IFormFieldProvider)
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
        """Check there are less than 7 published news articles marked
        as standout journalism in the past calendar week.

        This invariant only takes care of content being edited; content
        being published is checked within a workflow guard.
        """
        context = data.__context__
        if context is None:
            return  # adding an item, not editing it

        if not data.standout_journalism:
            return  # this is not standout journalism

        if api.content.get_state(context) != 'published':
            return  # item not published yet

        results = get_current_standout_journalism()
        # there should never be more than 7 items marked as
        # standout journalism at any given time
        assert len(results) <= 7
        # ignore current item if already marked as standout
        results = [o for o in results if o != context]
        if len(results) == 7:
            raise Invalid(_(
                u"Can't mark this item as standout. "
                u'There are already 7 items marked in the past calendar week.'
            ))
