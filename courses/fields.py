from curses.ascii import NUL
from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class OrderField(models.PositiveIntegerField):
    def __init__(self, for_fields=None, *args, **kvargs):
        self.for_fields = for_fields
        super.__init__(self, *args, **kvargs)
