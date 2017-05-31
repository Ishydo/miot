from django.conf.urls import url, include
from django.contrib import admin

from miot.views import page_views, poi_views, profile_views, static_views

urlpatterns = [
    url(r'^places', poi_views.PointOfInterestListView.as_view(), name="poi_list"),
    url(r'^p/(?P<slug>[-\w]+)/', poi_views.PointOfInterestDetailView.as_view(), name="poi_detail"),
    url(r'^dashboard$', profile_views.Dashboard.as_view(), name="dashboard"),
    url(r'^$', static_views.HomepageView.as_view(), name="homepage"),

    url(r'^dashboard/new/pointofinterest', poi_views.PointOfInterestCreateView.as_view(), name="poi_create"),
    url(r'^dashboard/new/page/(?P<slug>[-\w]+)', page_views.PageCreateView.as_view(), name="page_create"),
    url(r'^dashboard/new/page', poi_views.PointOfInterestSelectView.as_view(), name="poi_select"),
    url(r'^dashboard/delete/pointofinterest/(?P<slug>[-\w]+)', poi_views.PointOfInterestDeleteView.as_view(), name="poi_delete"),
    url(r'^dashboard/delete/page/(?P<slug>[-\w]+)', page_views.PageDeleteView.as_view(), name="page_delete"),
    url(r'^dashboard/edit/page/(?P<slug>[-\w]+)', page_views.PageUpdateView.as_view(), name="page_update"),
    url(r'^dashboard/edit/pointofinterest/(?P<slug>[-\w]+)', poi_views.PointOfInterestUpdateView.as_view(), name="poi_update"),


]
