
from django.views.generic import TemplateView
from django.shortcuts import render
from miot.models import PointOfInterest, Profile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

class Dashboard(LoginRequiredMixin, TemplateView):
    def get(self, request):
        context, context["pois"] = {}, request.user.profile.fetchPointOfInterests()
        context["pages"] = request.user.profile.fetchPages()
        context["API_KEY"] = settings.MAP_WIDGETS["GOOGLE_MAP_API_KEY"]
        hitsCounter = request.user.profile.fetchPointOfInterestsHits()
        context["total_hits"] = 0 if hitsCounter is None else hitsCounter["hits__sum"]
        return render(request, "dashboard/dashboard.html", context)
