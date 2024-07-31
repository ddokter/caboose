from django.db import models
from django.utils.translation import gettext_lazy as _


class Service(models.Model):

    """ Any added services to an event """

    name = models.CharField(_("Name"), max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):

        return self.name

    class Meta:
        app_label = "caboose"
        ordering = ["name"]
