from django.db import models
from django.utils.translation import gettext_lazy as _
from .facility import Facility


class Ship(models.Model):

    name = models.CharField(_("Name"), max_length=100)
    facility = models.ManyToManyField(Facility, blank=True,
                                      through="ShipFacility")

    def __str__(self):

        return self.name

    def list_facilities(self):

        return self.shipfacility_set.all()

    class Meta:

        app_label = "caboose"
        ordering = ["name"]


class ShipFacility(models.Model):

    ship = models.ForeignKey(Ship, on_delete=models.CASCADE)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    works_when_sailing = models.BooleanField(_("Works when sailing"),
                                             default=True)
