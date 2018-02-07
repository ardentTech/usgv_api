from django.db import models
from django.utils.translation import ugettext_lazy as _


class CreatedMixin(models.Model):
    created = models.DateTimeField(
        _("created"),
        auto_now_add=True)

    class Meta:
        abstract = True


class IsPublicMixin(models.Model):
    is_public = models.BooleanField(
        _("is public"),
        default=False)

    class Meta:
        abstract = True


class TitleMixin(models.Model):
    title = models.CharField(
        _("title"),
        max_length=128)

    class Meta:
        abstract = True


class UpdatedMixin(models.Model):
    updated = models.DateTimeField(
        _("updated"),
        auto_now=True)

    class Meta:
        abstract = True
