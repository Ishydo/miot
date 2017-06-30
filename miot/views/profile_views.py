
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
    def get(self, request):
        context, context["pois"] = {}, request.user.profile.fetch_points_of_interests()
        context["pages"] = request.user.profile.fetch_pages()
        context["API_KEY"] = settings.MAP_WIDGETS["GOOGLE_MAP_API_KEY"]
        hitsCounter = request.user.profile.fetch_points_of_interests_hits()
        context["total_hits"] = 0 if hitsCounter is None else hitsCounter["hits__sum"]

        # Getting beacons if app configured
        if request.user.profile.estimote_app_id is not None and request.user.profile.estimote_app_token is not None:
            context["nbBeacons"] = get_nb_beacon(request.user.profile)
            print(context["nbBeacons"])
            context["beacons"] = None if context["nbBeacons"] <= 0 else get_beacons(request.user.profile)
        else:
            context["beaconsToConfigure"] = True
        return render(request, "dashboard/dashboard.html", context)

class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model=Profile
    form_class=EstimoteAppForm
    template_name="dashboard/profile_form.html"
    success_url="/dashboard"
    success_message = "Profile updated successfully"

class StatisticsView(TemplateView):
    def get(self, request):
        context = {}
        context["visits"] = Page.objects.filter(poi__creator=request.user.profile)
        return render(request, "dashboard/statistics.html", context)

class ManageBeaconsView(TemplateView):
    def get(self, request):
        context = {}
        if request.user.profile.estimote_app_id is not None and request.user.profile.estimote_app_token is not None:
            context["beacons"] = get_beacons(request.user.profile)
        else:
            context["beaconsToConfigure"] = True
        return render(request, "dashboard/beacon_list.html", context)

class UpdateBeaconView(LoginRequiredMixin, TemplateView):
    def get(self, request, identifier):
        context, context["identifier"] = {}, identifier
        beacon = get_single_beacon(identifier, request.user.profile)
        context["beaconName"] = beacon["shadow"]["name"]
        context["beaconUrl"] = beacon["settings"]["advertisers"]["eddystone_url"][0]["url"]
        return render(request, "dashboard/beacon_edit.html", context=context)

    def post(self, request, identifier):
        bid = request.POST.get("beacon_identifier")
        bname = request.POST.get("beacon_name")
        burl = request.POST.get("beacon_url")
        if bid is not None and len(bname) > 3 and len(burl) >= 10:
            # Test update
            headers = {'Accept': 'application/json', "Content-Type": "application/json"}
            upd = {'shadow': {'name': bname}}
            upd2 = {"pending_settings": {"advertisers": {"eddystone_url": [{"index":1, "url": burl}]}}}
            u = requests.post("https://cloud.estimote.com/v2/devices/{0}".format(bid),
                    headers=headers,
                    auth=("{0}".format(request.user.profile.estimote_app_id), "{0}".format(request.user.profile.estimote_app_token)),
                    json=upd)
            v = requests.post("https://cloud.estimote.com/v2/devices/{0}".format(bid),
                    headers=headers,
                    auth=("miot-4lk", "9e14fb4f796324bb6bfac41a99a0f6aa"),
                    json=upd2)
            print(u.status_code)
            print(v.status_code)
            return redirect("dashboard")


def get_nb_beacon(profile):
    # Get the devices
    r = requests.get("https://cloud.estimote.com/v2/devices", auth=("{0}".format(profile.estimote_app_id), "{0}".format(profile.estimote_app_token)))
    beacons = json.loads(r.text)
    return len(beacons)

def get_single_beacon(identifier, profile):
    r = requests.get("https://cloud.estimote.com/v2/devices/{0}".format(identifier), auth=("{0}".format(profile.estimote_app_id), "{0}".format(profile.estimote_app_token)))
    return json.loads(r.text)

def get_beacons(profile):
    r = requests.get("https://cloud.estimote.com/v2/devices", auth=("{0}".format(profile.estimote_app_id), "{0}".format(profile.estimote_app_token)))
    return json.loads(r.text)
