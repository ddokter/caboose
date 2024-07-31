from django.views.generic import TemplateView
from django.urls import reverse
from django.http import HttpResponseRedirect
from ..models.task import Task


class Home(TemplateView):

    template_name = "index.html"

    def list_open_tasks(self):

        """ Get all open tasks for display on the dashboard."""

        return Task.objects.filter(status=0)

    def get(self, request, *args, **kwargs):

        if request.GET.get('task'):

            Task.objects.filter(id=request.GET.get('task')).update(status=1)

        return super().get(request, *args, **kwargs)
