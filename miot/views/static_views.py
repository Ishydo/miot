from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings

class HomepageView(TemplateView):
    def get(self, request):
        return render(request, "static/homepage.html", {"API_KEY": settings.MAP_WIDGETS["GOOGLE_MAP_API_KEY"]})
