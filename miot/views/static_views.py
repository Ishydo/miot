from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings
from miot.models import PointOfInterest

class HomepageView(TemplateView):
    '''The simple homepage view.'''
    def get(self, request):
        context, context["pois"] = {}, PointOfInterest.objects.all()[:5]
        return render(request, "static/homepage.html", context)

class AboutView(TemplateView):
    '''The static about view.'''
    def get(self, request):
        return render(request, "static/about.html")
