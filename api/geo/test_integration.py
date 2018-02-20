from django.core.urlresolvers import reverse

from geo.factories import UsStateFactory
from util.testing import BaseAPITestCase


class UsStateTestCase(BaseAPITestCase):

    endpoint = reverse("api:us-state-list")

    def test_get_ok(self):
        count = 3
        for i in range(count):
            UsStateFactory.create()
        response = self.client.get(self.endpoint)
        self.assert_get_ok(response, count=count)
