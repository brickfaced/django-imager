from django.test import TestCase
from .models import Album, Photo, User
from imager_profile.models import ImagerProfile
import factory
from random import choice
import datetime
time = datetime.datetime.now()
choices = (('PRIVATE', 'Private'), ('SHARED', 'Shared'), ('PUBLIC', 'Public'),)
choices2 = (('DSLR', 'Digital Single Lens Reflex'),
                                       ('M', 'Mirrorless'),
                                       ('AC', 'Advanced Compact'),
                                       ('SLR', 'Single Lens Reflex'))
choices1 = [('PRIVATE', 'Private'), ('SHARED', 'Shared'), ('PUBLIC', 'Public')]

def fake(user):
    user.profile.bio = factory.Faker('text').generate({})
    user.profile.phone = factory.Faker('phone_number').generate({})
    user.profile.location = factory.Faker('street_address').generate({})
    user.profile.website = factory.Faker('uri').generate({})
    user.profile.fee = factory.Faker('pyint').generate({})
    user.profile.is_active = factory.Faker('pybool').generate({})
    user.profile.camera = choice(choices)
    user.profile.save()
    return user

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')


class AlbomFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Album

    title = 'new_title'
    # published = choice(choices)
    date_created = datetime.datetime.now()
    date_modified = datetime.datetime.now()
    date_published = datetime.datetime.now()


class PhotoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Photo

    image = 'qwerty'
    title = '123345'
    # published = choice(choices)
    date_uploaded = datetime.datetime.now()
    date_modified = datetime.datetime.now()
    date_published = datetime.datetime.now()


class PhotoUnitTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestCase, cls)
        for _ in range(50):
            user = UserFactory.create()
            user.set_password(factory.Faker('password'))
            user.save()
            fake(user)       

            album = AlbomFactory.create(user=user)
            album.save()

            photo = PhotoFactory.create(album=album)
            photo.save()

    @classmethod
    def tearDownClass(cls):
        super(TestCase, cls)
        User.objects.all().delete()
    
    def test_albom_hase_user_and_cover_field(self):
        """check if required fields in albom class"""
        one_photo = Photo.objects.first() 
        self.assertIsNotNone(one_photo.album)
    
    def test_albom_class(self):
        """test if albom hase vreated date"""
        self.assertIsNotNone(Album.date_created)
   
    def test_photo_clss_image(self):
        """test image class path for image"""
        self.assertNotIsInstance(Photo.image, str)

    def test_photo_title(self):
        """test if imageproof phome type"""
        instance = Photo.objects.first()
        self.assertEqual(instance.title, '123345')
    
    # def test_imager_profile_bio(self):
    #     """test if albom hase date modified"""
    #     instance = Album.objects.first()
    #     self.assertIsInstance(instance.date_modified, time)   
