from django.test import TestCase

from .models import GVAIncident


class GVAIncidentTestCase(TestCase):

    def test_url_property(self):
        uid = 123456
        o = GVAIncident(gva_id=uid)
        self.assertEqual(o.url, GVAIncident.base_path + str(uid))
