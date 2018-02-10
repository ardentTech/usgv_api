from django.core.urlresolvers import reverse

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

    def test_get_filter_tag_ok(self):
        pass
