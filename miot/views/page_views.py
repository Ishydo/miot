from django.views.generic import CreateView, DeleteView, UpdateView
from miot.models import Page, PointOfInterest
from miot.forms import PointOfInterestForm, PageForm

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

class PageCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class=PageForm
    template_name = "dashboard/page_form.html"
    success_url="/dashboard"
    success_message = "%(title)s page was created successfully"

    def form_valid(self, form):
        form.instance.poi = PointOfInterest.objects.get(slug=self.kwargs["slug"])
        return super(PageCreateView, self).form_valid(form)

class PageUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Page
    form_class=PageForm
    template_name="dashboard/page_form.html"
    success_url="/dashboard"
    success_message = "%(title)s was updated successfully"

class PageDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Page
    template_name = "dashboard/page_delete.html"
    success_url = "/dashboard"
    success_message = "Page deleted successfully"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(PageDeleteView, self).delete(request, *args, **kwargs)
