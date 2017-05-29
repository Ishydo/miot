from django.views.generic import ListView, DetailView
from miot.models import PointOfInterest


class PointOfInterestListView(ListView):
    model = PointOfInterest
    template_name = "poi_list.html"

class PointOfInterestDetailView(DetailView):
    model = PointOfInterest
    template_name = "poi_detail.html"
    context_object_name = "poi"
