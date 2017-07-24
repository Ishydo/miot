from django.views.generic import CreateView, DeleteView, UpdateView, ListView, View, DetailView
from miot.models import Page, PointOfInterest
from miot.forms import PointOfInterestForm, PageForm
from django.http import HttpResponse
from django.db.models import F
from django.db import transaction

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt

from hitcount.views import HitCountDetailView

class PageDetailView(HitCountDetailView):
    '''The view for a page detail. It will display the page content and use the
    specific template that was chosen by the creator.'''
    model = Page
    template_name = "page_detail.html"
    count_hit = True

    def get_context_data(self, **kwargs):
        '''The get context data get the ordered pages in order to generate the
        navigation menu on the template.'''
        context = super(PageDetailView, self).get_context_data(**kwargs)
        context['ordered_pages'] = PointOfInterest.objects.get(slug=self.kwargs['slugPOI']).get_ordered_pages()
        return context

class PageManageListView(ListView):
    '''This views is used to see the list of pages that belong to the current user.'''
    model = Page
    template_name = "dashboard/page_list.html"

    def get_queryset(self):
        '''The queryset contains every pages in the points of interest of that user.'''
        return Page.objects.select_related().filter(poi__in=self.request.user.profile.fetch_points_of_interests())

class PoiPageUpdateView(LoginRequiredMixin, ListView):
    '''This page is used to display every page of a given point of interest
    belonging to the user.'''
    model = PointOfInterest
    template_name = "dashboard/manage-poi-pages.html"

    def get_context_data(self, **kwargs):
        '''The context data adds the slug of the poi to identify it.'''
        context = super(PoiPageUpdateView, self).get_context_data(**kwargs)
        context['poi'] = PointOfInterest.objects.get(slug=self.kwargs['slug'])
        return context

    def get_queryset(self):
        '''The get queryset fetch all the pages ordered by index for this poi.'''
        return Page.objects.filter(poi=PointOfInterest.objects.get(slug=self.kwargs['slug'])).order_by("index")

class PageCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    '''The page creation view.'''
    form_class=PageForm
    template_name = "dashboard/page_form.html"
    success_url="/dashboard"
    success_message = "%(title)s page was created successfully"

    def form_valid(self, form):
        '''When the form is valid, we set the point of interest of the created
        page and set the base index.'''
        form.instance.poi = PointOfInterest.objects.get(slug=self.kwargs["slug"])
        form.instance.index = Page.objects.filter(poi=form.instance.poi).count()
        return super(PageCreateView, self).form_valid(form)

class PageUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    '''The update page view.'''
    model = Page
    form_class=PageForm
    template_name="dashboard/page_form.html"
    success_url="/dashboard"
    success_message = "%(title)s was updated successfully"

class PageDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    '''The delete page view asking for confirmation on a specific template.'''
    model = Page
    template_name = "dashboard/page_delete.html"
    success_url = "/dashboard"
    success_message = "Page deleted successfully"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(PageDeleteView, self).delete(request, *args, **kwargs)


class ChangeOrder(View):
    '''The method called when pages are reordered on the poi page list view.
    This could probably be optimized.'''
    def post(self, request, *args, **kwargs):
        oldIndex = request.POST.get("oldIndex")
        newIndex = request.POST.get("newIndex")

        if newIndex > oldIndex:
            lPages = Page.objects.filter(poi=PointOfInterest.objects.get(pk=request.POST.get("poi")), index__lte=newIndex).filter(index__gte=oldIndex).exclude(index=oldIndex)
            lPages.update(index= F('index') - 1)
        else:
            lPages = Page.objects.filter(poi=PointOfInterest.objects.get(pk=request.POST.get("poi")), index__gte=newIndex).filter(index__lte=oldIndex).exclude(index=oldIndex)
            lPages.update(index= F('index') + 1)
        cPage = Page.objects.filter(poi=PointOfInterest.objects.get(pk=request.POST.get("poi")), index=oldIndex).order_by("last_updated")
        p = cPage.first()
        p.index=newIndex
        p.save()

        return HttpResponse("ok")
