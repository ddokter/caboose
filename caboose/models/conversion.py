from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from .unit import Unit


class ConversionQuerySet(models.QuerySet):

    def find_for_unit(self, unit):

        """Find conversions for the given unit. This will find conversion
        that have the unit as 'to' value and 'from' value.
        """

        return super().filter(Q(from_unit=unit) | Q(to_unit=unit))


class ConversionManager(models.Manager):

    def get_queryset(self):

        return ConversionQuerySet(self.model, using=self._db)


class Conversion(models.Model):

    from_amount = models.FloatField(_("From amount"), default=1.0)
    from_unit = models.ForeignKey(
        Unit, on_delete=models.CASCADE,
        related_name="conversion_set", verbose_name=_("From unit"))
    to_amount = models.FloatField(_("To amount"), default=1.0)
    to_unit = models.ForeignKey(
        Unit, on_delete=models.CASCADE,
        related_name="conversion_set_reverse", verbose_name=_("To unit"))
    ingredient = models.ManyToManyField("Ingredient", blank=True)
    generic = models.BooleanField(_("Generic"), default=False)

    # Set object manager
    objects = ConversionManager()

    def __str__(self):

        return "%.2f %s = %.2f %s (%s)" % (
            self.from_amount, self.from_unit,
            self.to_amount, self.to_unit,
            self.generic and "*" or self.ingredients_list)

    @property
    def ingredients_list(self):

        return ", ".join([str(item) for item in self.ingredient.all()])

    @property
    def amount(self):

        return self.to_amount / self.from_amount

    class Meta:

        app_label = "caboose"
        ordering = ["from_unit__name"]
