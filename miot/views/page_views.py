from django.views.generic import CreateView
from miot.models import Page, PointOfInterest
from miot.forms import PointOfInterestForm, PageForm

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin

class PageCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class=PageForm
    template_name = "dashboard/page_form.html"
    success_url="/dashboard"
    success_message = "%(title)s was created successfully"


    def form_valid(self, form):
        form.instance.poi = PointOfInterest.objects.get(slug=self.kwargs["slug"])
        return super(PageCreateView, self).form_valid(form)
