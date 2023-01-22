from django.test import TestCase
from base.models import Status


class StatusTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.status = Status.objects.create(title='Принято решение')

    def test_text_convert_to_slug(self):
        status = StatusTest.status
        slug = status.slug
        self.assertEqual(slug, 'prinyato-reshenie')
