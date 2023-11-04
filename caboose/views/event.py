from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseRedirect
from django.forms import inlineformset_factory
from .base import CreateView, UpdateView, DetailView
from ..models.event import Event
from ..forms.event import EventForm


class FormSetMixin:

    def get_form(self, form_class=None):

        form = super().get_form(form_class=form_class)

        form.fields.pop('recipe')
        form.fields.pop('extra')

        return form

    @property
    def formsets(self):

        factory1 = inlineformset_factory(Event, Event.recipe.through,
                                         exclude=[])

        factory2 = inlineformset_factory(Event, Event.extra.through,
                                         exclude=[])

        kwargs = {}

        if self.request.method == "POST":
            kwargs['data'] = self.request.POST

        if self.object:
            kwargs['instance'] = self.object

        return [factory1(**kwargs), factory2(**kwargs)]

    def form_valid(self, form):

        self.object = form.save()

        for _formset in self.formsets:

            if _formset.is_valid():
                _formset.save()

        return HttpResponseRedirect(self.get_success_url())


class EventCreateView(FormSetMixin, CreateView):

    model = Event
    form_class = EventForm
    fields = None


class EventUpdateView(FormSetMixin, UpdateView):

    model = Event
    form_class = EventForm
    fields = None


class EventShoppingListView(DetailView):

    model = Event
    template_name = "event_shopping_list.html"

    def list_warnings(self):

        warnings = []

        for recipe in self.object.list_recipes():

            if not recipe.has_ingredients:

                warnings.append((recipe, "No ingredients given"))

        return warnings
