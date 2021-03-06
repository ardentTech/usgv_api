from django.db import models
from django.utils.translation import ugettext_lazy as _

from util.models import CreatedMixin, UpdatedMixin


class GVAIncident(CreatedMixin, UpdatedMixin):

    base_path = "http://www.gunviolencearchive.org/incident/"

    date = models.DateField(
        _("date"))
    tags = models.ManyToManyField(
        "taxonomy.Tag",
        verbose_name=_("tags"))
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
    state = models.ForeignKey(
        "geo.UsState",
        verbose_name=_("US state"))
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

    @property
    def victims(self):
        return self.injured + self.killed
