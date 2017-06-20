from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save
from django_extensions.db.fields import AutoSlugField
from taggit.managers import TaggableManager
from django.contrib.gis.db import models as gmodels
from django.conf import settings
from django.dispatch import receiver
from hitcount.models import HitCountMixin
from hitcount.models import HitCount
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D

USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

class Profile(models.Model):
    user = models.OneToOneField(USER_MODEL, blank=True, null=True)
    estimote_app_id = models.CharField(max_length=120, blank=True, null=True)
    estimote_app_token = models.CharField(max_length=255, blank=True, null=True)

    def fetch_points_of_interests(self):
        return PointOfInterest.objects.filter(creator=self)

    def fetch_points_of_interests_hits(self):
        return HitCount.objects.select_related().filter(object_pk__in=self.fetch_points_of_interests()).aggregate(Sum("hits"))

    def fetch_pages(self):
        return Page.objects.select_related().filter(poi__in=self.fetch_points_of_interests())

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=120)
    slug = AutoSlugField(populate_from='name')
    emoji_name = models.CharField(max_length=100, blank=True, null=True)
    short_description = models.CharField(max_length=255)
    parent = models.ForeignKey('self', blank=True, null=True, related_name="children")

    def __str__(self):
        return self.name

class PointOfInterest(models.Model, HitCountMixin):
    name = models.CharField(max_length=120)
    slug = AutoSlugField(populate_from='name')
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    featured_image = models.ImageField(upload_to="uploads/poi")
    position = gmodels.PointField()
    tags = TaggableManager()
    active = models.BooleanField(default=True)
    creator = models.ForeignKey(Profile, null=True, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)

    def get_ordered_pages(self):
        return Page.objects.filter(poi=self).order_by("index")

    def __str__(self):
        return self.name

class Template(models.Model):
    name = models.CharField(max_length=120)
    slug = AutoSlugField(populate_from="name")
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    short_description = models.CharField(max_length=255)
    featured_image = models.ImageField(upload_to="uploads/templates")

    def __str__(self):
        return self.name

class Page(models.Model, HitCountMixin):
    title = models.CharField(max_length=120)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    content = models.TextField()
    poi = models.ForeignKey('PointOfInterest', on_delete=models.CASCADE)
    template = models.ForeignKey('Template', on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from="title")
    index = models.IntegerField(default=0)

    def __str__(self):
        return self.title

@receiver(post_save, sender=USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(post_save, sender=PointOfInterest)
def create_poi_page(sender, instance, created, **kwargs):
    if created:
        Page.objects.create(poi=instance, title="Homepage", content="Your content here.", template=Template.objects.first())


# utils
def get_near_poi(lat, long):
    location = Point(float(long), float(lat))
    return PointOfInterest.objects \
        .filter(position__distance_lte=(location, D(km=10))) \
        .annotate(distance=Distance('position', location)) \
        .order_by('distance')
