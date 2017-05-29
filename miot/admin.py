from django.contrib import admin
from miot.models import PointOfInterest, Page, Template, Category
from django.contrib.gis.db import models as gmodels
from mapwidgets.widgets import GooglePointFieldWidget

class PointOfInterestAdmin(admin.ModelAdmin):
    formfield_overrides = {
        gmodels.PointField: {"widget": GooglePointFieldWidget}
    }

admin.site.register(PointOfInterest, PointOfInterestAdmin)
admin.site.register(Page)
admin.site.register(Template)
admin.site.register(Category)
