from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.apps import apps
from .unit import Unit
from .conversion import Conversion
from .category import Category


class Ingredient(models.Model):

    """ Any basic ingredient for the preparation of food """

    name = models.CharField(_("Name"), max_length=100)
    synoniem = models.CharField(_("Synonyms"), blank=True, null=True,
                                max_length=100)
    default_unit = models.ForeignKey(
        Unit, on_delete=models.CASCADE,
        verbose_name=_("Default unit"))
    default_size = models.FloatField(_("Default size of unit"),
                                     blank=True, null=True)
    avg_pp = models.FloatField(_("Average per person in default units"),
                               blank=True, null=True)
    avg_price = models.FloatField(_("Average price per default unit/size"),
                                  blank=True, null=True)
    category = models.ManyToManyField(Category, blank=True)

    def __str__(self):

        return self.name

    def list_recipes(self):

        """ Find all recipes where this ingredient is used """

        ri_model = apps.get_model("caboose", "RecipeIngredient")
        recipe_model = apps.get_model("caboose", "Recipe")

        recipe_ids = ri_model.objects.filter(
            ingredient=self).values_list("recipe__id", flat=True)

        return recipe_model.objects.filter(id__in=recipe_ids)

    def list_conversions(self):

        """ Return all conversions for this ingredient """

        return Conversion.objects.filter(ingredient=self)

    def get_price(self, unit, amount):

        """Return the price for the given unit and amount. If the unit
        differs from the default unit, see if there is a conversion.

        """

        # TODO: what if there is no default size? It is not required.

        conv_factor = 1

        if unit != self.default_unit:

            conv_factor = unit.find_conversion_path(
                self.default_unit, self).result

        return conv_factor * self.avg_price * (amount / self.default_size)

    @property
    def categories(self):

        """ List categories for this ingredient """

        return self.category.all()

    class Meta:
        app_label = "caboose"
        ordering = ["name"]
