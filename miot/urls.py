from django.conf.urls import url, include
from django.contrib import admin

from miot.views import poi_views, profile_views, static_views

urlpatterns = [
    url(r'^places', poi_views.PointOfInterestListView.as_view(), name="poi_list"),
    url(r'^p/(?P<slug>[-\w]+)/', poi_views.PointOfInterestDetailView.as_view(), name="poi_detail"),
    url(r'^dashboard', profile_views.Dashboard.as_view(), name="dashboard"),
    url(r'^$', static_views.HomepageView.as_view(), name="homepage")
]
