from django.core.urlresolvers import reverse

from crime.factories import GVAIncidentFactory
from util.testing import BaseAPITestCase


class GVAIncidentTestCase(BaseAPITestCase):

    endpoint = reverse("api:gva-incident-list")

    def test_get_ok(self):
        count = 3
        for i in range(count):
            GVAIncidentFactory.create()
        response = self.client.get(self.endpoint)
        self.assert_get_ok(response, count=count)
