from django.test import TestCase
from django.contrib.auth.models import User

from miot.models import Template, Category, Profile

class TemplateTestCase(TestCase):
    def create_template(self):
        return Template.objects.create(name="TestTemplate", short_description="Test template descrpition.")

    def test_template_creation(self):
        t = self.create_template()
        self.assertTrue(isinstance(t, Template))
        self.assertEqual(t.name, "TestTemplate")

class UserTestCase(TestCase):
    def create_user(self):
        return User.objects.create(username="Bryan", email="bryan@bryan.com", password="password")

    def test_user_profile_creation(self):
        u = self.create_user()
        self.assertTrue(isinstance(u.profile, Profile))
        self.assertEqual(u.profile.user, u)
        self.assertEqual(u.username, "Bryan")

class CategoryTestCase(TestCase):
    def create_category(self):
        return Category.objects.create(name="Food", short_description="Food stuff.")

    def test_category_creation(self):
        c = self.create_category()
        self.assertTrue(isinstance(c, Category))
        self.assertEqual(c.name, "Food")
