""" Task definitions """

from django.db import models
from django.utils.translation import gettext_lazy as _


PRIO_VOCAB = [(1, _("High")),
              (3, _("Medium")),
              (5, _("Low"))]

STATUS_VOCAB = [(0, _("Open")),
                (1, _("Done")),
                (2, _("Cancelled")),
                (3, _("Forfeited"))]


class Task(models.Model):

    """ Base task implementation """

    name = models.CharField(_("Name"), max_length=100)
    description = models.TextField(_("Description"), blank=True, null=True)
    priority = models.SmallIntegerField(default=3,
                                        choices=PRIO_VOCAB)
    status = models.SmallIntegerField(default=0,
                                      editable=False,
                                      choices=STATUS_VOCAB)

    @property
    def is_done(self):

        """ Shortcut to done status """

        return self.status == 1

    def __str__(self):

        return self.name

    def get_details(self):

        """ Return a more detailed description of the task. This should
        be a tuple of (str, dict) """

        return (self.description, {})

    class Meta:
        app_label = "caboose"
