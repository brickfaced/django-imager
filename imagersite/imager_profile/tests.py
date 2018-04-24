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


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ImagerProfile
    
    bio = factory.Faker('text')
    phone = factory.Faker('phone_number')
    location = factory.Faker('street_address')
    website = factory.Faker('uri')
    fee = factory.Faker('pyint')
    is_active = factory.Faker('pybool')
    camera = choice(choices)


class ProfileUnitTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestCase, cls)
        for _ in range(50):
            user = UserFactory.create()
            user.set_password(factory.Faker('password'))
            user.save()

            profile = ProfileFactory.create(user=user)
            profile.save()
            
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
        number = User.objects.all()
        self.assertEqual(len(number), 50)