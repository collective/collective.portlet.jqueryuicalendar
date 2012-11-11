import json
from zope.interface import implements

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from zope.formlib import form

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.utils import DT2dt

class IjQueryUICalendarPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    # TODO: Add any zope.schema fields here to capture portlet configuration
    # information. Alternatively, if there are no settings, leave this as an
    # empty interface - see also notes around the add form and edit form
    # below.

    # some_field = schema.TextLine(title=_(u"Some field"),
    #                              description=_(u"A field to use"),
    #                              required=True)


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IjQueryUICalendarPortlet)

    # TODO: Set default values for the configurable parameters here

    # some_field = u""

    # TODO: Add keyword parameters for configurable parameters here
    # def __init__(self, some_field=u""):
    #    self.some_field = some_field

    def __init__(self):
        pass

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return "jQueryUI Calendar Portlet"


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('jqueryuicalendarportlet.pt')

    def all_events_json(self):
        return "var allEventsJSON = %s" % json.dumps(self.all_events())

    def all_events(self):
        query = self.get_query()
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog(**query)
        events = {}
        for brain in brains:
            start = DT2dt(brain.start)
            start_str = start.strftime('%Y-%m-%d')
            if start_str not in events:
                events[start_str] = []
            events[start_str].append({'uid': brain.UID,
                                      'title': brain.Title,
                                      'description': brain.Description,
                                      'start': start_str,
                                      'end': brain.end.strftime('%Y-%m-%d')})
        return events

    def get_query(self):
        return {'portal_type': 'Event',
                'review_state': 'published',
                'sort_on': 'start',
                'sort_order': 'reverse',
                'sort_limit': 1000}

class AddForm(base.NullAddForm):
    """Portlet add form.
    """
    def create(self):
        return Assignment()


