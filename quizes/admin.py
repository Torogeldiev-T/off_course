from django.contrib import admin
from .models import *


class AnswerInline(admin.TabularInline):
    model = Answer


class QustionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]


admin.site.register(Quiz)
admin.site.register(Question, QustionAdmin)
admin.site.register(Answer)
admin.site.register(Result)
