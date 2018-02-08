from django.db import models
from django.utils.translation import ugettext_lazy as _

from localflavor.us.models import USStateField


class GVAIncident(models.Model):

    date = models.DateTimeField(
        _("date"))
    city_county = models.CharField(
        _("city or county"),
        max_length=128)
    gva_id = models.PositiveIntegerField(
        _("GVA ID"))
    injured = models.PositiveIntegerField(
        _("# injured"))
    killed = models.PositiveIntegerField(
        _("# killed"))
    state = USStateField(
        _("us state"))
    street = models.CharField(
        _("steet"),
        max_length=128)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return str(self.date)
