from datetime import date, timedelta
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from .recipe import Recipe
from .ingredient import Ingredient
from .ship import Ship


GROUP_TYPE_VOCAB = [(0.9, '<15'),
                    (1.0, 'Mixed'),
                    (1.2, '15-25'),
                    (0.8, '60+')]


MEAL_VOCAB = [(0, 'Breakfast'), (1, 'Lunch'), (2, 'Diner'), (3, 'Other')]


class Event(models.Model):

    """Represent any event, that is basically a collection of
    recipes"""

    name = models.CharField(_("Name"), max_length=100, blank=True, null=True)
    from_date = models.DateField()
    to_date = models.DateField()
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE,
                             blank=True, null=True)
    groupsize = models.SmallIntegerField(_("Group size"))
    grouptype = models.FloatField(
        _("Group composition (avg)"),
        default=1.0,
        choices=GROUP_TYPE_VOCAB
    )
    recipe = models.ManyToManyField(Recipe, through="EventRecipe")
    extra = models.ManyToManyField(Ingredient, through="EventIngredient")
    notes = models.TextField(_("Notes"), blank=True, null=True)
    plan = models.TextField(_("Plan"), blank=True, null=True)
    evaluation = models.TextField(_("Evaluation"), blank=True, null=True)

    services = models.ManyToManyField(
        "Service", blank=True, null=True, through="EventService")

    def __str__(self):

        try:
            period = (f"{self.from_date.strftime('%d %B %Y')} -\n"
                      f"{self.to_date.strftime('%d %B %Y')}"
                      )
        except AttributeError:
            period = ""

        return f"{self.name or ''} {period} ({self.groupsize} pers.)"

    def list_recipes(self):

        """ All recipes for this event """

        return self.recipe.all()

    def get_schedule(self):

        """ Return the day-by-day schedule for this trip """

        date = self.from_date
        dates = []

        while date <= self.to_date:

            dates.append(date)

            date += timedelta(days=1)

        return dates

    def list_extras(self):

        return self.extra.all()

    def list_services(self):

        return self.services.all()

    def generate_shopping_list(self):

        ingredients = {}

        # TODO: account for different units!
        # TODO: add units to dict, instead of using default units,
        # in case there is no conversion

        for evt_recipe in self.eventrecipe_set.all():

            recipe = evt_recipe.recipe

            resize_factor = (self.groupsize / recipe.servings) \
                * evt_recipe.amount * self.grouptype

            for rec_ingredient in recipe.list_ingredients():

                conv_factor = 1

                if (
                        rec_ingredient.unit !=
                        rec_ingredient.ingredient.default_unit):

                    try:

                        conv_factor = rec_ingredient.unit.find_conversion_path(
                            rec_ingredient.ingredient.default_unit,
                            rec_ingredient.ingredient).result
                    except IndexError:

                        conv_factor = -1

                if rec_ingredient.ingredient in ingredients:
                    ingredients[rec_ingredient.ingredient] \
                        += (rec_ingredient.calculated_amount * resize_factor *
                            conv_factor)
                else:
                    ingredients[rec_ingredient.ingredient] \
                        = (rec_ingredient.calculated_amount * resize_factor *
                           conv_factor)

        # Add extra's
        #
        for evt_ingredient in self.eventingredient_set.all():

            conv_factor = 1

            if (
                    evt_ingredient.unit !=
                    evt_ingredient.ingredient.default_unit):

                try:

                    conv_factor = evt_ingredient.unit.find_conversion_path(
                        evt_ingredient.ingredient.default_unit,
                        evt_ingredient.ingredient).result
                except IndexError:

                    conv_factor = -1

            if evt_ingredient.ingredient in ingredients:
                ingredients[evt_ingredient.ingredient] \
                    += (evt_ingredient.amount * conv_factor)
            else:
                ingredients[evt_ingredient.ingredient] \
                    = evt_ingredient.amount * conv_factor

        return ingredients

    def get_cost(self):

        """ Generate total cost, if possible """

        total = 0

        for recipe in self.list_recipes():

            status, sub, errors = recipe.price_pp

            total += sub * self.groupsize * self.grouptype

        return total

    def get_cost_pp(self):

        """ Return cost per person """

        return self.get_cost() / self.groupsize

    @property
    def archived(self):

        """ Determine whether this event is in the past."""

        return self.to_date < date.today()

    def get_safe_plan(self):

        """ Mark the plan safe, so as to be able to show it as is. """

        return mark_safe(self.plan)

    def get_safe_notes(self):

        """ Mark the notes safe, so as to be able to show it as is. """

        return mark_safe(self.notes)

    class Meta:
        ordering = ["-from_date", "-to_date"]
        app_label = "caboose"
        verbose_name = _("Event")
        verbose_name_plural = _("Events")


class EventRecipe(models.Model):

    """ Relate recipes to events """

    amount = models.FloatField(_("Amount"))
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    day = models.SmallIntegerField(null=True, blank=True)
    meal = models.SmallIntegerField(null=True, blank=True, default=3,
                                    choices=MEAL_VOCAB)

    def __str__(self):

        return f"{self.ingredient} {self.amount}"

    @property
    def is_facilitated(self):

        """Do the facilities needed for the recipe match the facilities
        offered?

        """

        if self.event.ship:

            ship_facilities = self.event.ship.facility.values_list('id',
                                                                   flat=True)
            return self.recipe.facility.filter(
                id__in=ship_facilities).exists() or \
                not self.recipe.facility.exists()

        return False

    class Meta:

        app_label = 'caboose'
        ordering = ['day', 'meal']


class EventIngredient(models.Model):

    """ Extra ingredients for the shopping list """

    amount = models.FloatField(_("Amount"))
    unit = models.ForeignKey("Unit", on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)


class EventService(models.Model):

    """ Event services """

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    service = models.ForeignKey("Service", on_delete=models.CASCADE)
