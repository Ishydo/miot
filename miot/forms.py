from mapwidgets.widgets import GooglePointFieldWidget
from miot.models import PointOfInterest, Page, Profile
from django import forms

class PointOfInterestForm(forms.ModelForm):
    class Meta:
        model = PointOfInterest
        fields = ("name", "featured_image", "position", "tags", "active", "category")
        widgets = {
            'position': GooglePointFieldWidget,
        }

class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ("title", "content", "template")

class EstimoteAppForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("estimote_app_id", "estimote_app_token")
