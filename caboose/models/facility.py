from django.db import models
from django.utils.translation import gettext_lazy as _


class Facility(models.Model):

    name = models.CharField(_("Name"), max_length=100)

    def __str__(self):

        return self.name

    class Meta:

        app_label = "caboose"
        ordering = ["name"]
        verbose_name_plural = _("Facilities")
