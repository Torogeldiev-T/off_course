from curses.ascii import NUL
from turtle import mode
from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class OrderField(models.PositiveIntegerField):
    def __init__(self, for_fields=None, *args, **kvargs):
        self.for_fields = for_fields
        super.__init__(*args, **kvargs)

    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) is None:
            # no current value
            try:
                # filter by objects with the same field values
                # for the fields in "for_fields"
                qs = model_instance.objects.all()
                if self.for_fields:
                    query = {
                        field: getattr(model_instance, field)
                        for field in self.for_fields
                    }
                    qs.filter(**query)
                # get the order of the last item
                last_item = qs.latest(self.attname)
                value = last_item.order + 1
            except ObjectDoesNotExist:
                value = 0
                setattr(model_instance, self.attname, value)
                return value
        else:
            return super().pre_save(model_instance, add)
