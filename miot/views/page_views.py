from django.views.generic import CreateView, DeleteView, UpdateView, ListView, View, DetailView
from miot.models import Page, PointOfInterest
from miot.forms import PointOfInterestForm, PageForm
from django.http import HttpResponse
from django.db.models import F

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt

class PageDetailView(DetailView):
    model = Page
    template_name = "page_detail.html"

    def get_context_data(self, **kwargs):
        context = super(PageDetailView, self).get_context_data(**kwargs)
        context['ordered_pages'] = PointOfInterest.objects.get(slug=self.kwargs['slugPOI']).getOrderedPages()
        return context

class PageManageListView(ListView):
    model = Page
    template_name = "dashboard/page_list.html"

    def get_queryset(self):
        return Page.objects.select_related().filter(poi__in=self.request.user.profile.fetchPointOfInterests())

class PoiPageUpdateView(LoginRequiredMixin, ListView):
    model = PointOfInterest
    template_name = "dashboard/manage-poi-pages.html"

    def get_context_data(self, **kwargs):
        context = super(PoiPageUpdateView, self).get_context_data(**kwargs)
        context['poi'] = PointOfInterest.objects.get(slug=self.kwargs['slug'])
        return context

    def get_queryset(self):
        return Page.objects.filter(poi=PointOfInterest.objects.get(slug=self.kwargs['slug'])).order_by("index")

class PageCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class=PageForm
    template_name = "dashboard/page_form.html"
    success_url="/dashboard"
    success_message = "%(title)s page was created successfully"

    def form_valid(self, form):
        form.instance.poi = PointOfInterest.objects.get(slug=self.kwargs["slug"])
        form.instance.index = Page.objects.filter(poi=form.instance.poi).count()
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


class ChangeOrder(View):
    def post(self, request, *args, **kwargs):
        oldIndex = request.POST.get("oldIndex")
        newIndex = request.POST.get("newIndex")

        if newIndex > oldIndex:
            ps = Page.objects.filter(poi=PointOfInterest.objects.get(pk=request.POST.get("poi")), index__lte=newIndex)
            ps.update(index= F('index') - 1)
        else:
            pass
        return HttpResponse("ok")
