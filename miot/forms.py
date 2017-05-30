from mapwidgets.widgets import GooglePointFieldWidget
from miot.models import PointOfInterest
from django import forms

class PointOfInterestForm(forms.ModelForm):
    class Meta:
        model = PointOfInterest
        fields = ("name", "featured_image", "position", "tags", "active")
        widgets = {
            'position': GooglePointFieldWidget,
        }

        def form_valid(self, form):
            form.instance.creator = self.request.user
            return super(PointOfInterestForm, self).form_valid(form)
