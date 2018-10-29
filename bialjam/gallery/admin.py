from django.contrib import admin
from .models import Directory, Image


class InlineImage(admin.TabularInline):
    model = Image


class DirectoryAdmin(admin.ModelAdmin):
    inlines = [InlineImage]


admin.site.register(Directory, DirectoryAdmin)
