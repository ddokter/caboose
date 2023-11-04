from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):

    """Category for ingredient, so as to be able to 'superclass' them."""

    name = models.CharField(_("Name"), max_length=100)
    synonyms = models.CharField(_("Synonyms"), max_length=255,
                                null=True, blank=True)
    icon = models.CharField(_("Icon"), blank=True, null=True, max_length=50)

    def __str__(self):

        return self.name

    @property
    def byline(self):

        return self.synonyms

    def list_materials(self):

        return self.ingredient_set.all()

    class Meta:
        app_label = "caboose"
        ordering = ["name"]
        verbose_name_plural = _("Categories")
