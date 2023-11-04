from django.apps import AppConfig
from django.forms import widgets


def render(self, name, value, attrs=None, renderer=None):

    """Render the widget as an HTML string."""

    context = self.get_context(name, value, attrs)

    template_name = 'django/forms/widgets/select.html'

    if name.endswith("ingredient"):
        template_name = "widgets/select.html"

    return self._render(template_name, context, renderer)


class CabooseConfig(AppConfig):

    name = 'caboose'

    def ready(self):

        # widgets.Select.render = render
        pass
