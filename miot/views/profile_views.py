
from django.views.generic import TemplateView, UpdateView
from django.shortcuts import render, redirect
from miot.models import PointOfInterest, Profile, Page
from miot.forms import EstimoteAppForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.conf import settings

import requests
import json

class Dashboard(LoginRequiredMixin, TemplateView):
    '''The administration dashboard view.'''
    def get(self, request):
        # Get the user's points of interest
        context, context["pois"] = {}, request.user.profile.fetch_points_of_interests()
        # Get the user's pages
        context["pages"] = request.user.profile.fetch_pages()
        # Get the google map api key
        context["API_KEY"] = settings.MAP_WIDGETS["GOOGLE_MAP_API_KEY"]
        # Get the last point of interest created
        context["lastPOI"] = context["pois"].last()
        # Get the total number of visits
        hitsCounter = request.user.profile.fetch_points_of_interests_hits()
        context["total_hits"] = 0 if hitsCounter["hits__sum"] is None else hitsCounter["hits__sum"]

        # Getting beacons if app configured
        if request.user.profile.estimote_app_id is not None and request.user.profile.estimote_app_token is not None:
            context["nbBeacons"] = get_nb_beacon(request.user.profile)
            context["beacons"] = None if context["nbBeacons"] <= 0 else get_beacons(request.user.profile)
        else:
            context["beaconsToConfigure"] = True
        return render(request, "dashboard/dashboard.html", context)

class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    '''The small profile update view.'''
    model=Profile
    form_class=EstimoteAppForm
    template_name="dashboard/profile_form.html"
    success_url="/dashboard"
    success_message = "Profile updated successfully"

class StatisticsView(TemplateView):
    '''The statistics view.'''
    def get(self, request):
        context = {}
        context["visits"] = Page.objects.filter(poi__creator=request.user.profile)
        return render(request, "dashboard/statistics.html", context)

class ManageBeaconsView(TemplateView):
    '''The view on which user can manage beacons.'''
    def get(self, request):
        context = {}
        if request.user.profile.estimote_app_id is not None and request.user.profile.estimote_app_token is not None:
            context["beacons"] = get_beacons(request.user.profile)
        else:
            context["beaconsToConfigure"] = True
        return render(request, "dashboard/beacon_list.html", context)

class UpdateBeaconView(LoginRequiredMixin, TemplateView):
    '''The view for a beacon update through the estimote API.'''
    def get(self, request, identifier):
        context, context["identifier"] = {}, identifier
        beacon = get_single_beacon(identifier, request.user.profile)
        context["beaconName"] = beacon["shadow"]["name"]
        context["beaconUrl"] = beacon["settings"]["advertisers"]["eddystone_url"][0]["url"]
        context["pois"] = PointOfInterest.objects.filter(creator=request.user.profile)
        return render(request, "dashboard/beacon_edit.html", context=context)

    def post(self, request, identifier):
        '''When it is a post on the view, we trigger the API calls to preconfigure
        the concerned beacon in order to add pending settings to it.'''
        bid = request.POST.get("beacon_identifier")
        bname = request.POST.get("beacon_name")
        burl = request.POST.get("beacon_url")
        # If settings are valid
        if bid is not None and len(bname) > 3 and len(burl) >= 10:
            # Set the headers
            headers = {'Accept': 'application/json', "Content-Type": "application/json"}
            # The update data
            upd = {'shadow': {'name': bname}}
            upd2 = {"pending_settings": {"advertisers": {"eddystone_url": [{"index":1, "url": burl}]}}}
            # The API requests
            u = requests.post("https://cloud.estimote.com/v2/devices/{0}".format(bid),
                    headers=headers,
                    auth=("{0}".format(request.user.profile.estimote_app_id), "{0}".format(request.user.profile.estimote_app_token)),
                    json=upd)
            v = requests.post("https://cloud.estimote.com/v2/devices/{0}".format(bid),
                    headers=headers,
                    auth=("{0}".format(request.user.profile.estimote_app_id), "{0}".format(request.user.profile.estimote_app_token)),
                    json=upd2)
            return redirect("dashboard")


def get_nb_beacon(profile):
    '''Get the number of beacon devices attached to this user.'''
    # Get the devices
    r = requests.get("https://cloud.estimote.com/v2/devices", auth=("{0}".format(profile.estimote_app_id), "{0}".format(profile.estimote_app_token)))
    beacons = json.loads(r.text)
    return len(beacons) if beacons is not None else 0

def get_single_beacon(identifier, profile):
    '''Get a single beacon informations.'''
    r = requests.get("https://cloud.estimote.com/v2/devices/{0}".format(identifier), auth=("{0}".format(profile.estimote_app_id), "{0}".format(profile.estimote_app_token)))
    return json.loads(r.text)

def get_beacons(profile):
    '''Get all beacons informations.'''
    r = requests.get("https://cloud.estimote.com/v2/devices", auth=("{0}".format(profile.estimote_app_id), "{0}".format(profile.estimote_app_token)))
    return json.loads(r.text)
