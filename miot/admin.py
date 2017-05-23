from django.contrib import admin
from miot.models import PointOfInterest, Page, Template, Category


class PointOfInterestAdmin(admin.ModelAdmin):
    fields = ('name', 'featured_image', 'position', 'active', 'tags')

admin.site.register(PointOfInterest, PointOfInterestAdmin)
admin.site.register(Page)
admin.site.register(Template)
admin.site.register(Category)
