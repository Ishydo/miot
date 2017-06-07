from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from miot.models import PointOfInterest
from miot.forms import PointOfInterestForm
from django.utils.safestring import mark_safe

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

class PointOfInterestDiscoverView(ListView):
    model = PointOfInterest
    template_name ="poi_list.html"


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

class PointOfInterestUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model=PointOfInterest
    form_class=PointOfInterestForm
    template_name="dashboard/poi_form.html"
    success_url="/dashboard"
    success_message = "%(name)s was updated successfully"

class PointOfInterestDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = PointOfInterest
    template_name = "dashboard/poi_delete.html"
    success_url = "/dashboard"
    success_message = "Point of Interest was deleted successfully"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(PointOfInterestDeleteView, self).delete(request, *args, **kwargs)

class PointOfInterestSelectView(LoginRequiredMixin, ListView):
    template_name="dashboard/select_poi.html"
    def get_queryset(self):
        return PointOfInterest.objects.filter(creator=self.request.user.profile)
