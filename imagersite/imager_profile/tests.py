from django.test import TestCase
from .models import ImagerProfile, User
import factory
from random import randint, choice


choices = (('DSLR', 'Digital Single Lens Reflex'),
                                       ('M', 'Mirrorless'),
                                       ('AC', 'Advanced Compact'),
                                       ('SLR', 'Single Lens Reflex'))
choices1 = ["('DSLR', 'Digital Single Lens Reflex')",
                                       "('M', 'Mirrorless')",
                                       "('AC', 'Advanced Compact')",
                                       "('SLR', 'Single Lens Reflex')"]


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')

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

class ProfileUnitTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestCase, cls)
        for _ in range(50):
            user = UserFactory.create()
            user.set_password(factory.Faker('password'))
            user.save()
            fake(user)
            
    def setUpUser(self):
        self.user = UserFactory.create(user_name='codefellows')
        self.user.set_password('secret')
        self.user.save()

    @classmethod
    def tearDownClass(cls):
        super(TestCase, cls)
        User.objects.all().delete()

    def test_user_can_see_its_profile(self):
        """test if user hase prof value"""
        one_user = User.objects.first()
        self.assertIsNotNone(one_user.profile)

    def test_imager_profile(self):
        """test if imagerprof hase bio"""
        self.assertIsNotNone(ImagerProfile.bio)
   
    def test_imager_profile_phone(self):
        """test if imageproof hase phone"""
        self.assertNotIsInstance(ImagerProfile.bio, int)

    def test_imager_profile_phone_qqqq(self):
        """test if imageproof phome type"""
        instance = ImagerProfile.objects.first()
        self.assertIsInstance(instance.phone, str)
    
    def test_imager_profile_bio(self):
        """test if imageproof hase bio"""
        instance = ImagerProfile.objects.first()
        self.assertIsInstance(instance.bio, str)    

    def test_imager_profile_fee(self):
        """test if imageproof hase fee"""
        instance = ImagerProfile.objects.first()
        self.assertIsInstance(instance.fee, float)

    def test_imager_profile_(self):
        """test if imageproof hase """
        instance = ImagerProfile.objects.first()
        self.assertIn(instance.camera, choices1)

    def test_number_of_records(self):
        """test quantity of osers"""
        number = User.objects.all()
        self.assertEqual(len(number), 50)