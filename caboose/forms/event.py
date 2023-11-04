from django import forms
from django.forms import ModelForm
from ..models import Event


class DateInput(forms.DateInput):

    input_type = 'date'


class EventForm(ModelForm):

    """ Override form for date widget """

    class Meta:
        model = Event
        fields = "__all__"
        widgets = {
            'from_date': DateInput(),
            'to_date': DateInput(),
        }
