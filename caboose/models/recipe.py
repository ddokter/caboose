"""All recipe related stuff, like the model and the relation model to
ingredients

"""

import json
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import F
from .unit import Unit
from .ingredient import Ingredient
from .facility import Facility
from .tag import Tag
from .allergen import Allergen


class Recipe(models.Model):

    """The recipe lists ingredients and may describe how to create
    the dish. A recipe may hold sub recipes, so as to be able to
    describe more complex dishes that are a combination of other
    dishes

    """

    name = models.CharField(_("Name"), max_length=100)
    source = models.CharField(_("Source"), max_length=100, blank=True,
                              null=True)
    descr = models.CharField(_("Description"), max_length=200)
    servings = models.SmallIntegerField(_("Servings"))
    ingredient = models.ManyToManyField(Ingredient, through="RecipeIngredient")
    notes = models.TextField(_("Notes"), blank=True, null=True)
    beer_pairing = models.TextField(_("Beer pairing"), blank=True, null=True)
    facility = models.ManyToManyField(Facility, blank=True, null=True)
    tag = models.ManyToManyField(Tag, blank=True, null=True)
    subs = models.ManyToManyField("self", blank=True, null=True,
                                  symmetrical=False)
    alt = models.ManyToManyField(Ingredient, through="AltIngredient",
                                 related_name="alt",
                                 through_fields=("recipe", "alternative"))
    price_json = models.TextField(editable=False, null=True)

    def __str__(self):

        return self.name

    @property
    def has_ingredients(self):

        """ Do we really have ingredients? """

        return self.recipeingredient_set.exists()

    def list_alts(self):

        """ List alternative ingredients """

        return self.altingredient_set.all()

    def list_ingredients(self, _filter=None, exclude=None, servings=None):

        """List all ingredients, use filter if there. Also list
        ingredients of subs. Make sure to convert subs to proper
        servings.

        """

        if not servings:
            servings = self.servings

        if not exclude:
            exclude = []

        base = self.recipeingredient_set.filter(**(_filter or {})).annotate(
            calculated_amount=F("amount") * (float(servings) /
                                             F("recipe__servings")))

        exclude.append(self.id)

        for sub in self.subs.all().exclude(id__in=exclude):

            sub_qs = sub.list_ingredients(_filter=_filter, exclude=exclude,
                                          servings=self.servings)

            base = base.union(sub_qs)

        return base

    def list_facilities(self, exclude=None):

        """ What facilities are needed for the recipe """

        if not exclude:
            exclude = []

        exclude.append(self.id)

        base = self.facility.all()

        for sub in self.subs.all().exclude(id__in=exclude):

            base.union(sub.list_facilities(exclude=[self.id]))

        return base

    @property
    def price_pp(self):

        """ Return price per person or list of errors """

        if not self.price_json:

            self.save()

        return json.loads(self.price_json)

    @property
    def price_pp_opt(self):

        """Return price per person or list of errors for optional
        ingredients

        """

        return self.get_price(_filter={'optional': True})

    def get_price(self, _filter=None):

        """ Calculate price, taking sub recipes into account """

        errors = []
        total = 0
        status = 0

        for rec_ingredient in self.list_ingredients(_filter=_filter):

            try:
                total += rec_ingredient.ingredient.get_price(
                    rec_ingredient.unit,
                    rec_ingredient.calculated_amount)
            except IndexError:
                status = -1
                errors.append(str(rec_ingredient))

        return (status, total / self.servings, errors)

    def list_allergens(self):

        """ Return a list of all allergens, based on the allergens in the
        ingredients of this recipe """

        ingredient_ids = [ingredient.ingredient.id for ingredient in
                          self.recipeingredient_set.all()]

        return Allergen.objects.filter(
            ingredient__in=ingredient_ids).distinct()

    def save(self, *args, **kwargs):

        """Override save to set calculated price. Check whether we
        already have an id.

        """

        if self.id:
            self.price_json = json.dumps(self.get_price())

        return super().save(*args, **kwargs)

    class Meta:
        ordering = ["name"]
        app_label = "caboose"
        verbose_name = _("Recipe")
        verbose_name_plural = _("Recipes")


class RecipeIngredient(models.Model):

    """ Relate ingredients to recipe, with a given amount and unit """

    # TODO: make sure that there is a conversion from given unit to
    # ingredient's default unit

    amount = models.FloatField(_("Amount"))
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    optional = models.BooleanField(_("Optional"), default=False)

    @property
    def amount_avg(self):

        return self.recipe.servings * self.ingredient.avg_pp

    @property
    def price(self):

        """ Calculate price for the given amount """

        try:
            return self.ingredient.get_price(self.unit, self.amount)
        except IndexError:
            return None

    def __str__(self):

        return f"{ self.ingredient } { self.amount }"


class AltIngredient(models.Model):

    """ Alternatives and their effect """

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    alternative = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                    null=True, blank=True,
                                    related_name="alternative")
    substitutes = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                    related_name="substitutes")
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE,
                            null=True, blank=True)

    def __str__(self):

        base = f"Instead of { self.substitutes } use { self.alternative }"

        if self.tag:
            base += f" to make it { self.tag }"

        return base
