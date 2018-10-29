from django.contrib import admin


# Register your models here.
from .models import Vip, Lesson
admin.site.register(Vip)
admin.site.register(Lesson)
