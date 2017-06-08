from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings
from miot.models import PointOfInterest

class HomepageView(TemplateView):
    def get(self, request):
        context, context["pois"] = {}, PointOfInterest.objects.all()[:5]
        return render(request, "static/homepage.html", context)
