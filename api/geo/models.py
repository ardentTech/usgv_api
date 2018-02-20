from django.db import models
from django.utils.translation import ugettext_lazy as _


class UsState(models.Model):

    fips_code = models.CharField(
        _("FIPS code"),
        max_length=2)
    name = models.CharField(
        _("Name"),
        max_length=64)
    postal_code = models.CharField(
        _("USPS code"),
        max_length=2)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
