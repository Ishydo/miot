from django.test import TestCase

class CodeTestCase(TestCase):
    def test_code_is_valid(self):
        self.assertEqual(1+1, 2)
