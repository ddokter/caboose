from math import inf
from django.db import models
from django.db.models import Q
from django.apps import apps
from django.utils.translation import gettext_lazy as _
from caboose.path import Path, UnresolvableExpression


# Do not seek any deeper than this... more conversions is probably a
# very unreliable path anyway.
#
MAX_DEPTH = 10

# Set the minimum precision needed as percentage/100 of the best
# result found. Only paths with a precision better than this are kept.
#
MIN_PRECISION = 0.8

# Set maximum path length as a factor of the shortest path found. Any
# paths longer than this will be discarded.
#
MAX_PATH_LENGTH = 2


class Unit(models.Model):

    """Any possible unit for ingredients, be it weight, volume or
    whatever."""

    name = models.CharField(_("Name"), max_length=100)

    def __str__(self):

        return self.name

    def find_conversion_path(self, unit, ingredient, _filter=None,
                              _exclude=None, stack=None):

        """Find all possible conversion paths from self to the given unit. The
        returned list will be sorted on path length, shortest path
        first.

        """

        return list(self._find_conversion_paths(
            unit, ingredient, _filter=_filter, _exclude=_exclude,
            _stack=stack))[0]

    def _find_conversion_paths(self, unit, ingredient, _filter=None,
                               _exclude=None, _stack=None):

        """Use breath-first to find the shortest paths for the
        conversion asked. The search will only be performed up to
        MAX_DEPTH, to prevent long searches for non existing
        conversions. Whenever a path is found, only paths where length
        is within the boundaries set by MAX_PATH_LENGTH are
        considered.

        """

        conv_model = apps.get_model("caboose", "Conversion")

        if _stack:
            path = Path(self, unit, ingredient)
            for conv in _stack:
                path.append(conv)
            stack = [(_stack[0].to_unit, path)]
        else:
            stack = [(self, Path(self, unit, ingredient))]

        # If last conversion on path is already what we are looking
        # for, yield this! Also, return since it looks like we're not
        # interested in more results...
        #
        if (_stack and (_stack[0].to_unit == unit or
                        _stack[0].from_unit == unit)):

            yield stack[0][1]
            return

        # Set shortest to infinity
        #
        shortest = inf

        # Keep track of end points of the paths under scrutiny. Any
        # new end-point that is less precise than this, is discarded.
        #
        while stack:

            (last_unit, path) = stack.pop(0)

            # Whenever the paths are getting too long, call it a day.
            #
            if len(path) + 1 > shortest * MAX_PATH_LENGTH:
                break

            # stop whenever MAX_DEPTH is reached
            #
            if len(path) > MAX_DEPTH:
                break

            qs = conv_model.objects.exclude(id__in=[conv.id for conv in path])

            qs = qs.filter(Q(generic=True) | Q(ingredient=ingredient))

            qs = qs.find_for_unit(last_unit).distinct()

            if _filter:
                qs = qs.filter(**_filter)

            if _exclude:
                qs = qs.exclude(**_exclude)

            qs = qs.prefetch_related("to_unit", "from_unit")

            for conv in qs:

                try:
                    # We have a terminal conversion!
                    #
                    if conv.to_unit == unit or conv.from_unit == unit:

                        new_path = path.copy()
                        new_path.append(conv)

                        shortest = min(len(new_path), shortest)

                        yield new_path

                    else:
                        new_path = path.copy()
                        new_path.append(conv)

                        if conv.to_unit == last_unit:
                            end_unit = conv.from_unit
                        else:
                            end_unit = conv.to_unit

                        # Discard conversions over different quantities
                        #
                        # if(conv.from_unit.quantity != conv.to_unit.quantity):
                        #    continue

                        stack.append((end_unit, new_path))

                except UnresolvableExpression:

                    # forget about this conversion...

                    pass

    class Meta:

        app_label = "caboose"
        ordering = ["name"]
        verbose_name_plural = _("Units")
