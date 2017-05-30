from django.views.generic import ListView, DetailView, CreateView
from miot.models import PointOfInterest
from miot.forms import PointOfInterestForm

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin

class PointOfInterestListView(ListView):
    model = PointOfInterest
    template_name = "poi_list.html"

class PointOfInterestDetailView(DetailView):
    model = PointOfInterest
    template_name = "poi_detail.html"
    context_object_name = "poi"

class PointOfInterestCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class=PointOfInterestForm
    template_name = "dashboard/poi_form.html"
    success_url="/dashboard"
    success_message = "%(name)s was created successfully"
