import datetime

from django.core.urlresolvers import reverse

from crime.factories import GVAIncidentFactory
from geo.factories import UsStateFactory
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

    def test_get_filter_date_exact_ok(self):
        date1 = datetime.date.today()
        date2 = date1 - datetime.timedelta(days=5)
        GVAIncidentFactory.create(date=date1)
        GVAIncidentFactory.create(date=date2)

        response = self.client.get(self.endpoint + "?date={0}".format(date1))
        self.assert_get_ok(response, count=1)

    def test_get_filter_date_year_ok(self):
        pass

    def test_get_filter_state_exact_ok(self):
        state1 = UsStateFactory.create()
        state2 = UsStateFactory.create()
        GVAIncidentFactory.create(state=state1)
        GVAIncidentFactory.create(state=state2)

        response = self.client.get(self.endpoint + "?state={0}".format(state1.id))
        self.assert_get_ok(response, count=1)

    def test_get_filter_tag_exact_ok(self):
        tag1 = TagFactory.create()
        tag2 = TagFactory.create()
        GVAIncidentFactory.create(tags=(tag1,))
        GVAIncidentFactory.create(tags=(tag2,))

        response = self.client.get(self.endpoint + "?tags={0}".format(tag1.id))
        self.assert_get_ok(response, count=1)

    def test_get_yearly_stats_ok(self):
        today = datetime.date.today()
        one_year_ago = today - datetime.timedelta(days=365)
        state1 = UsStateFactory.create()
        state2 = UsStateFactory.create()
        state3 = UsStateFactory.create()

        GVAIncidentFactory.create(
            date=one_year_ago,
            injured=5,
            killed=7,
            state=state1)
        GVAIncidentFactory.create(
            date=one_year_ago,
            injured=6,
            killed=8,
            state=state1)
        GVAIncidentFactory.create(
            date=today,
            injured=6,
            killed=8,
            state=state2)
        GVAIncidentFactory.create(
            date=today,
            injured=7,
            killed=9,
            state=state3)

        response = self.client.get(reverse("api:gva-incident-yearly-stats"))
        self.assert_get_ok(response, count=3)

    def test_get_years_ok(self):
        today = datetime.date.today()
        one = GVAIncidentFactory.create(date=today - datetime.timedelta(days=365))
        two = GVAIncidentFactory.create(date=today)
        response = self.client.get(reverse("api:gva-incident-years"))
        self.assert_get_ok(response)
        self.assertEqual(self.get_content(response), [one.date.year, two.date.year])


#class GVAStatsTestCase(BaseAPITestCase):
#
#    endpoint = reverse("gva-stats")
#
#    def test_get_explicit_year_ok(self):
#        for i in range(5):
#            GVAIncidentFactory.create()
#        response = self.client.get(self.endpoint)
#        self.assert_get_ok(response)
#
#        today = datetime.date.today()
#        state = UsStateFactory.create()
#
#        GVAIncidentFactory.create(date=today, state=state)
#        GVAIncidentFactory.create(date=(today - datetime.timedelta(days=365)), state=state)
#
#        response = self.client.get(self.endpoint + "?year={}".format(today.year))
#        self.assert_get_ok(response)
#        self.assertEqual(self.get_content(response)[0]["incidents"], 1)
#
#    def test_get_default_year_ok(self):
#        today = datetime.date.today()
#        state = UsStateFactory.create()
#
#        GVAIncidentFactory.create(date=today, state=state)
#        GVAIncidentFactory.create(date=(today - datetime.timedelta(days=365)), state=state)
#
#        response = self.client.get(self.endpoint)
#        self.assert_get_ok(response)
#        self.assertEqual(self.get_content(response)[0]["incidents"], 1)
#
#    def test_get_no_state_ok(self):
#        today = datetime.date.today()
#        count = 3
#        for i in range(count):
#            GVAIncidentFactory.create(date=today)
#
#        response = self.client.get(self.endpoint)
#        self.assert_get_ok(response)
#        self.assertEqual(self.get_content(response)[0]["incidents"], count)
#
#    def test_get_explicit_state_ok(self):
#        today = datetime.date.today()
#        state = UsStateFactory.create()
#        GVAIncidentFactory.create(date=today, state=state)
#        GVAIncidentFactory.create(date=today)
#
#        response = self.client.get(self.endpoint + "?state={}".format(state.id))
#        self.assert_get_ok(response)
#        self.assertEqual(self.get_content(response)[0]["incidents"], 1)
