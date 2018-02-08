from django.db import models
from django.utils.translation import ugettext_lazy as _

from localflavor.us.models import USStateField
from util.models import CreatedMixin, UpdatedMixin


class GVAIncident(CreatedMixin):

    base_path = "http://www.gunviolencearchive.org/incident/"

    date = models.DateTimeField(
        _("date"))
    categories = models.ManyToManyField(
        "crime.GVAIncidentCategory",
        verbose_name=_("categories"))
    city_county = models.CharField(
        _("city or county"),
        max_length=128)
    gva_id = models.PositiveIntegerField(
        _("GVA ID"),
        unique=True)
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

    @property
    def url(self):
        return self.base_path + str(self.gva_id)


class GVAIncidentCategory(CreatedMixin, UpdatedMixin):

    name = models.CharField(
        _("name"),
        max_length=128,
        unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
