from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
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

    def form_valid(self, form):
        form.instance.creator = self.request.user.profile
        return super(PointOfInterestCreateView, self).form_valid(form)

class PointOfInterestUpdateView(UpdateView):
    model=PointOfInterest
    form_class=PointOfInterestForm
    template_name="dashboard/poi_form.html"

class PointOfInterestDeleteView(DeleteView):
    model = PointOfInterest
    template_name = "dashboard/poi_delete.html"
    success_url = "/dashboard"
    success_message = "%(name)s was created successfully"
