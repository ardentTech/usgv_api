from django.core.urlresolvers import reverse

from crime.factories import GVAIncidentFactory, GVAIncidentCategoryFactory
from util.testing import BaseAPITestCase


class GVAIncidentTestCase(BaseAPITestCase):

    endpoint = reverse("api:gva-incident-list")

    def test_get_ok(self):
        count = 3
        category = GVAIncidentCategoryFactory.create()
        for i in range(count):
            GVAIncidentFactory.create(categories=(category,))
        response = self.client.get(self.endpoint)
        self.assert_get_ok(response, count=count)
