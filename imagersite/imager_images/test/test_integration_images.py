from django.test import TestCase
from imager_profile.models import User
from ..models import Album, Photo
from model_mommy import mommy
import tempfile
import factory
from random import choice

choices = (('PRIVATE', 'Private'), ('SHARED', 'Shared'), ('PUBLIC', 'Public'),)


class TestStoreRoutes(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestCase, cls)

        for n in range(10):
            user = mommy.make(User)
            user.set_password('password')
            user.save()
            user.profile.bio = factory.Faker('text').generate({})
            user.profile.phone = factory.Faker('phone_number').generate({})
            user.profile.location = factory.Faker('street_address').generate({})
            user.profile.website = factory.Faker('uri').generate({})
            user.profile.fee = factory.Faker('pyint').generate({})
            user.profile.is_active = factory.Faker('pybool').generate({})
            user.profile.camera = choice(choices)
            user.profile.save()
            album = mommy.make(Album, user=user)
            mommy.make(Photo, album=album, image=tempfile.NamedTemporaryFile(suffix='.png').name)
    
    @classmethod
    def tearDownClass(cls):
        User.objects.all().delete()
        super(TestCase, cls)

    def test_200_status_on_authenticated_request_to_store(self):
        """test status from library"""
        user = User.objects.first()
        # self.client.login(username=user.username, password='password')
        # import pdb; pdb.set_trace()
        self.client.force_login(user)
        response = self.client.get('/images/library')
        self.client.logout()
        self.assertEqual(response.status_code, 200)

    # def test_200_status_on_authenticated_request_to_picture(self):
    #     """test status from library"""
    #     user = User.objects.first()
    #     self.client.force_login(user)
    #     response = self.client.get('/picture/')
    #     self.client.logout()
    #     self.assertEqual(response.status_code, 200)
        
    # def test_200_status_on_authenticated_request_to_album(self):
    #     """test status from library"""
    #     user = User.objects.first()
    #     self.client.force_login(user)
    #     response = self.client.get('/album/')
    #     self.client.logout()
    #     self.assertEqual(response.status_code, 200)
