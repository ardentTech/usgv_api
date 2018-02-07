import json

from rest_framework import status
from rest_framework.test import APITestCase


class BaseAPITestCase(APITestCase):

    def assert_bad_request(self, response):
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def assert_get_ok(self, response, **kwargs):
        count = kwargs.get("count", 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if count > 0:
            self.assertEqual(self.get_content(response)["count"], count)

    def assert_not_found(self, response):
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def assert_post_ok(self, response):
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def get_content(self, response):
        return json.loads(response.content.decode("utf-8"))
