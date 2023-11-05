from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseRedirect
from django.forms import inlineformset_factory
from .base import CreateView, UpdateView
from caboose.models.ship import Ship


class FormSetMixin:

    def get_form(self, form_class=None):

        form = super().get_form(form_class=form_class)

        form.fields.pop('facility')

        return form

    @property
    def formset_label(self):

        return _("Facilities")

    @property
    def formsets(self):

        """ Make formsets a property, for easy access in templates """

        factory = inlineformset_factory(Ship, Ship.facility.through,
                                        exclude=[])

        kwargs = {}

        if self.request.method == "POST":
            kwargs['data'] = self.request.POST

        if self.object:
            kwargs['instance'] = self.object

        return [factory(**kwargs)]

    def form_valid(self, form):

        """ Validate form and formsets """

        self.object = form.save()

        for _formset in self.formsets:

            if _formset.is_valid():
                _formset.save()

        return HttpResponseRedirect(self.get_success_url())


class ShipCreateView(FormSetMixin, CreateView):

    model = Ship


class ShipUpdateView(FormSetMixin, UpdateView):

    model = Ship
