from django.conf.urls import url, include
from django.contrib import admin

from miot.views import page_views, poi_views, profile_views, static_views

urlpatterns = [
    # Routes related to the frontend (discover in two modes and about)
    url(r'^places$', poi_views.PointOfInterestListViewPos.as_view(), name="poi_list"),
    url(r'^map$', poi_views.PointOfInterestListViewMap.as_view(), name="poi_map"),
    url(r'^about$', static_views.AboutView.as_view(), name="about"),

    # The dashboard related routes
    url(r'^dashboard/$', profile_views.Dashboard.as_view(), name="dashboard"),

    # Routes for the creation of a new object
    url(r'^dashboard/new/pointofinterest', poi_views.PointOfInterestCreateView.as_view(), name="poi_create"),
    url(r'^dashboard/new/page/(?P<slug>[-\w]+)', page_views.PageCreateView.as_view(), name="page_create"),
    url(r'^dashboard/new/page', poi_views.PointOfInterestSelectView.as_view(), name="poi_select"),

    # Routes for the deletion of an object
    url(r'^dashboard/delete/pointofinterest/(?P<slug>[-\w]+)', poi_views.PointOfInterestDeleteView.as_view(), name="poi_delete"),
    url(r'^dashboard/delete/page/(?P<slug>[-\w]+)', page_views.PageDeleteView.as_view(), name="page_delete"),

    # Routes for the updates of an object
    url(r'^dashboard/edit/page/(?P<slug>[-\w]+)', page_views.PageUpdateView.as_view(), name="page_update"),
    url(r'^dashboard/edit/pages/(?P<slug>[-\w]+)', page_views.PoiPageUpdateView.as_view(), name="poi_page_update"),
    url(r'^dashboard/edit/beacon/(?P<identifier>[-\w]+)', profile_views.UpdateBeaconView.as_view(), name="beacon_update"),
    url(r'^dashboard/edit/profile/(?P<pk>[-\w]+)', profile_views.ProfileUpdateView.as_view(), name="profile_update"),
    url(r'^dashboard/edit/pointofinterest/(?P<slug>[-\w]+)', poi_views.PointOfInterestUpdateView.as_view(), name="poi_update"),

    # Route to manage lists
    url(r'^dashboard/switch$', page_views.ChangeOrder.as_view(), name="switch_page_order"),
    url(r'^dashboard/manage/pages$', page_views.PageManageListView.as_view(), name="page_manage"),
    url(r'^dashboard/manage/pointofinterests$', poi_views.PointOfInterestManageListView.as_view(), name="poi_manage"),
    url(r'^dashboard/manage/beacons$', profile_views.ManageBeaconsView.as_view(), name="beacon_manage"),
    url(r'^dashboard/statistics$', profile_views.StatisticsView.as_view(), name="statistics"),

    # Routes for the detailviews
    url(r'^p/(?P<slugPOI>[-\w]+)/(?P<slug>[-\w]+)', page_views.PageDetailView.as_view(), name="page_detail"),
    url(r'^p/(?P<slug>[-\w]+)/', poi_views.PointOfInterestDetailView.as_view(), name="poi_detail"),

    # Homepage
    url(r'^$', static_views.HomepageView.as_view(), name="homepage"),

]
