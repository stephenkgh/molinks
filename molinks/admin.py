from django.contrib import admin

from .models import Category, Link


class LinkInline(admin.TabularInline):
    model = Link
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    inlines = [LinkInline]
    # TODO: organize by User, default to logged in user?

admin.site.register(Category, CategoryAdmin)
