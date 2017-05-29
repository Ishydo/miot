from django.db import models
from django_extensions.db.fields import AutoSlugField
from taggit.managers import TaggableManager
from django.contrib.gis.db import models as gmodels

class Category(models.Model):
    name = models.CharField(max_length=120)
    slug = AutoSlugField(populate_from='name')
    emoji_name = models.CharField(max_length=100, blank=True, null=True)
    short_description = models.CharField(max_length=255)
    parent = models.ForeignKey('self', blank=True, null=True, related_name="children")

    def __str__(self):
        return self.name

class PointOfInterest(models.Model):
    name = models.CharField(max_length=120)
    slug = AutoSlugField(populate_from='name')
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    featured_image = models.ImageField(upload_to="uploads/poi")
    position = gmodels.PointField()
    tags = TaggableManager()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Template(models.Model):
    name = models.CharField(max_length=120)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    short_description = models.CharField(max_length=255)
    featured_image = models.ImageField(upload_to="uploads/templates")

    def __str__(self):
        return self.name

class Page(models.Model):
    title = models.CharField(max_length=120)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    content = models.TextField()
    poi = models.ForeignKey('PointOfInterest', on_delete=models.CASCADE)
    template = models.ForeignKey('Template', on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from="title")

    def __str__(self):
        return self.title
