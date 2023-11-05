from django.db import models
from django.utils.translation import gettext_lazy as _


class Allergen(models.Model):

    """Allergen for ingredient, so as to be able to 'superclass' them."""

    name = models.CharField(_("Name"), max_length=100)

    def __str__(self):

        return self.name

    def list_materials(self):

        return self.ingredient_set.all()

    class Meta:
        app_label = "caboose"
        ordering = ["name"]
        verbose_name_plural = _("Allergens")
