from django.shortcuts import render
from django.views.generic import TemplateView

class HomepageView(TemplateView):
    def get(self, request):
        return render(request, "static/homepage.html")
