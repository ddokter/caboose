from django.db import models
from django.utils.translation import gettext_lazy as _


TAG_COLOR_VOCAB = [
    ("primary", "Blauw"),
    ("secondary", "Grijs"),
    ("success", "Groen"),
    ("warning", "Geel"),
    ("info", "Cyaan"),
    ("light", "Zwart"),
    ("dark", "Wit")
    ]


class Tag(models.Model):

    """ To be used to mark recipes """

    name = models.CharField(_("Name"), max_length=100)
    color = models.CharField(
        _("Tag color"),
        default="info",
        choices=TAG_COLOR_VOCAB,
        max_length=20
    )

    def __str__(self):

        return self.name

    class Meta:
        app_label = "caboose"
        ordering = ["name"]
        verbose_name_plural = _("Tags")
