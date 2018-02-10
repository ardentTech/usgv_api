import datetime

from django.core.urlresolvers import reverse

from localflavor.us.us_states import STATES_NORMALIZED

from crime.factories import GVAIncidentFactory
from taxonomy.factories import TagFactory
from util.testing import BaseAPITestCase


class GVAIncidentTestCase(BaseAPITestCase):

    endpoint = reverse("api:gva-incident-list")

    def test_get_ok(self):
        count = 3
        tag = TagFactory.create()
        for i in range(count):
            GVAIncidentFactory.create(tags=(tag,))
        response = self.client.get(self.endpoint)
        self.assert_get_ok(response, count=count)

    def test_get_filter_date_ok(self):
        date1 = datetime.date.today()
        date2 = datetime.date.today() - datetime.timedelta(days=5)
        GVAIncidentFactory.create(date=date1)
        GVAIncidentFactory.create(date=date2)

        response = self.client.get(self.endpoint + "?date={0}".format(date1))
        self.assert_get_ok(response, count=1)

    def test_get_filter_state_ok(self):
        state1 = STATES_NORMALIZED["colorado"]
        state2 = STATES_NORMALIZED["california"]
        GVAIncidentFactory.create(state=state1)
        GVAIncidentFactory.create(state=state2)

        response = self.client.get(self.endpoint + "?state={0}".format(state1))
        self.assert_get_ok(response, count=1)

    def test_get_filter_tag_ok(self):
        tag1 = TagFactory.create()
        tag2 = TagFactory.create()
        GVAIncidentFactory.create(tags=(tag1,))
        GVAIncidentFactory.create(tags=(tag2,))

        response = self.client.get(self.endpoint + "?tags={0}".format(tag1.id))
        self.assert_get_ok(response, count=1)
