from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, TemplateView
from miot.models import PointOfInterest, Page, Profile, Category, get_near_poi
from miot.forms import PointOfInterestForm
from django.utils.safestring import mark_safe
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import Q
from hitcount.views import HitCountDetailView
from hitcount.models import HitCount

from functools import reduce

from django.core.exceptions import PermissionDenied, ObjectDoesNotExist

class OwnerMixin(object):
    '''Mixin used to test if the current modified object is belonging to the
    current user.'''
    def get_object(self, queryset=None):
        """Returns the object the view is displaying."""
        if queryset is None:
            queryset = self.get_queryset()
        slug = self.kwargs.get("slug", None)
        queryset = queryset.filter(slug=slug,creator=self.request.user.profile)
        try:
            obj = queryset.get()
        except ObjectDoesNotExist:
            raise PermissionDenied
        return obj


class PointOfInterestListViewMap(ListView):
    '''The list view of points of interest but in map mode.'''
    template_name="poi_list_map.html"
    model = PointOfInterest

    def get_queryset(self):
        result = super(PointOfInterestListViewMap, self).get_queryset()
        # If we have a request or a given category
        if ("q" in self.request.GET and self.request.GET.get("q") != "") or "c" in self.request.GET:
            query = self.request.GET.get("q")
            # If the query is not empty
            if query is not None and query != "":
                # We split the words
                query_list = query.split()
                # And get the results
                result = PointOfInterest.objects.filter(
                           reduce(lambda x, y: x | y, [Q(name__icontains=word) for word in query_list]) |
                           (Q(tags__name__in=query_list))
                           ).distinct()
            if self.request.GET.get("c") != "all":
                result = result.filter(category__id=self.request.GET.get("c"))
            return result
        else:
            result = PointOfInterest.objects.filter(active=True)
            if self.request.GET.get("c") != "all" and "c" in self.request.GET:
                result = result.filter(category__id=self.request.GET.get("c"))
            return result

    def get_context_data(self, **kwargs):
        context = super(PointOfInterestListViewMap, self).get_context_data(**kwargs)
        # Get the most visted points of interest
        context["bestPois"] = sorted(PointOfInterest.objects.filter(active=True)[:3], key=lambda p: p.hit_count.hits, reverse=True)
        # Get the categories to display the select input
        context["categories"] = Category.objects.all
        # If we have the position
        if self.request.GET.get("lat") is not None:
            context["pois"] = get_near_poi(self.request.GET.get("lat"), self.request.GET.get("lon"))
        if self.request.GET.get("q") is not None:
            context["search"] = True
        return context


class PointOfInterestListViewPos(ListView):
    '''The list view of points of interest in classic list mode.'''
    paginate_by = 4
    template_name="poi_list.html"
    model = PointOfInterest

    def get_queryset(self):
        result = super(PointOfInterestListViewPos, self).get_queryset()
        if ("q" in self.request.GET and self.request.GET.get("q") != "") or "c" in self.request.GET:
            query = self.request.GET.get("q")
            if query is not None and query != "":
                query_list = query.split()
                result = PointOfInterest.objects.filter(
                           reduce(lambda x, y: x | y, [Q(name__icontains=word) for word in query_list]) |
                           (Q(tags__name__in=query_list))
                           ).distinct()
            if self.request.GET.get("c") != "all":
                result = result.filter(category__id=self.request.GET.get("c"))
            return result
        else:
            result = PointOfInterest.objects.filter(active=True)
            if self.request.GET.get("c") != "all" and "c" in self.request.GET:
                result = result.filter(category__id=self.request.GET.get("c"))
            return result

    def get_context_data(self, **kwargs):
        context = super(PointOfInterestListViewPos, self).get_context_data(**kwargs) # get the default context data
        context["bestPois"] = sorted(PointOfInterest.objects.filter(active=True)[:3], key=lambda p: p.hit_count.hits, reverse=True)
        context["topTags"] = PointOfInterest.tags.most_common()[:10]
        context["categories"] = Category.objects.all()
        if self.request.GET.get("lat") is not None:
            context["nearPois"] = get_near_poi(self.request.GET.get("lat"), self.request.GET.get("lon"))
        if "q" in self.request.GET or "c" in self.request.GET:
            context["search"] = True
        return context

class PointOfInterestManageListView(LoginRequiredMixin, OwnerMixin, ListView):
    '''The view of a list of the user's points of interest.'''
    model = PointOfInterest
    template_name = "dashboard/poi_list.html"

    def get_queryset(self):
        return self.request.user.profile.fetch_points_of_interests()

class PointOfInterestDetailView(HitCountDetailView):
    '''Detail view of a point of interest.'''
    model = PointOfInterest
    template_name = "poi_detail.html"
    context_object_name = "poi"
    count_hit = True

    def get_context_data(self, **kwargs):
        '''We need the orderded pages to display the navigation menu.'''
        context = super(PointOfInterestDetailView, self).get_context_data(**kwargs) # get the default context data
        context['ordered_pages'] = self.get_object().get_ordered_pages()
        return context

class PointOfInterestCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    '''View for a point of interest creation.'''
    form_class=PointOfInterestForm
    template_name = "dashboard/poi_form.html"
    success_url="/dashboard"
    success_message = "<strong>%(name)s</strong> point of interest was successfully created."

    def form_valid(self, form):
        '''When the form is valid we set the current user as the creator and send
        a success message.'''
        form.instance.creator = self.request.user.profile
        messages.add_message(self.request, messages.INFO, "Page successfully created", extra_tags='poi_created')
        return super(PointOfInterestCreateView, self).form_valid(form)

class PointOfInterestUpdateView(LoginRequiredMixin, OwnerMixin, SuccessMessageMixin, UpdateView):
    '''Update view of a poit of interest.'''
    model=PointOfInterest
    form_class=PointOfInterestForm
    template_name="dashboard/poi_form.html"
    success_url="/dashboard"
    success_message = "%(name)s was updated successfully"

class PointOfInterestDeleteView(LoginRequiredMixin, OwnerMixin, SuccessMessageMixin, DeleteView):
    '''Delete view for point of interest asking for a confirmation.'''
    model = PointOfInterest
    template_name = "dashboard/poi_delete.html"
    success_url = "/dashboard"
    success_message = "Point of Interest was deleted successfully"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(PointOfInterestDeleteView, self).delete(request, *args, **kwargs)

class PointOfInterestSelectView(LoginRequiredMixin, OwnerMixin, ListView):
    '''A list of the user's point of interest to select to which one a page must be added.'''
    template_name="dashboard/select_poi.html"
    def get_queryset(self):
        return PointOfInterest.objects.filter(creator=self.request.user.profile)
