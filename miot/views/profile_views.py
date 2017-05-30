
from django.views.generic import TemplateView
from django.shortcuts import render
from miot.models import PointOfInterest, Profile
from django.contrib.auth.mixins import LoginRequiredMixin


class Dashboard(LoginRequiredMixin, TemplateView):
    def get(self, request):
        context, context["pois"] = {}, request.user.profile.fetchPointOfInterests()
        context["pages"] = request.user.profile.fetchPages()
        return render(request, "dashboard/dashboard.html", context)
