from django.contrib import admin
from miot.models import PointOfInterest, Page, Template, Category, Profile
from django.contrib.gis.db import models as gmodels
from mapwidgets.widgets import GooglePointFieldWidget

class PointOfInterestAdmin(admin.ModelAdmin):
    formfield_overrides = {
        gmodels.PointField: {"widget": GooglePointFieldWidget}
    }

# Registering the models to be accessible in admin
admin.site.register(PointOfInterest, PointOfInterestAdmin)
admin.site.register(Page)
admin.site.register(Template)
admin.site.register(Category)
admin.site.register(Profile)
