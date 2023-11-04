from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseRedirect
from django.forms import inlineformset_factory
from django import forms
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import FormView
from ..models.recipe import Recipe
from .base import CreateView, UpdateView, CTypeMixin


class FormSetMixin:

    def get_form(self, form_class=None):

        form = super().get_form(form_class=form_class)

        form.fields.pop('ingredient')
        form.fields.pop('alt')

        return form

    @property
    def formset_label(self):

        return _("Ingredients")

    @property
    def formsets(self):

        factory1 = inlineformset_factory(Recipe, Recipe.ingredient.through,
                                         exclude=[])

        factory2 = inlineformset_factory(Recipe, Recipe.alt.through,
                                         exclude=[])

        kwargs = {}

        if self.request.method == "POST":
            kwargs['data'] = self.request.POST

        if self.object:
            kwargs['instance'] = self.object

        factory1_inst = factory1(**kwargs)

        return [factory1_inst, factory2(**kwargs)]

    def form_valid(self, form):

        self.object = form.save()

        for _formset in self.formsets:

            if _formset.is_valid():
                _formset.save()

        return HttpResponseRedirect(self.get_success_url())


class RecipeCreateView(FormSetMixin, CreateView):

    model = Recipe


class RecipeUpdateView(FormSetMixin, UpdateView):

    model = Recipe


class ConvertForm(forms.Form):

    persons = forms.IntegerField(
        label=_("Persons"),
    )


class RecipeConvertView(FormView, SingleObjectMixin, CTypeMixin):

    template_name = "recipe_convert.html"
    model = Recipe
    form_class = ConvertForm
    data = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):

        form = super().get_form(form_class=form_class)

        return form

    def form_valid(self, form):

        self.data = []

        resize_factor = form.cleaned_data['persons'] / self.object.servings

        for ingredient in self.object.list_ingredients():

            self.data.append((ingredient,
                              ingredient.amount * resize_factor,
                              (ingredient.price or 0) * resize_factor))

        return self.render_to_response(self.get_context_data(form=form))
