from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User, Goods
from decimal import Decimal

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertFalse(self.user.is_blacklisted)

class GoodsModelTest(TestCase):
    def setUp(self):
        self.goods = Goods.objects.create(
            title='Test Product',
            price=Decimal('99.99'),
            img_url='https://example.com/image.jpg'
        )

    def test_goods_creation(self):
        self.assertEqual(self.goods.title, 'Test Product')
        self.assertEqual(self.goods.price, Decimal('99.99'))

class UserRegistrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')

    def test_user_registration(self):
        data = {
            'username': 'newuser',
            'password': 'ValidPass123',
            'password2': 'ValidPass123'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

class GoodsViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )
        self.goods = Goods.objects.create(
            title='Test Product',
            price=Decimal('99.99'),
            img_url='https://example.com/image.jpg'
        )
        self.goods_url = reverse('goods-list-create')

    def test_get_goods_list_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.goods_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class PurchasesTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )
        self.goods = Goods.objects.create(
            title='Test Product',
            price=Decimal('99.99'),
            img_url='https://example.com/image.jpg'
        )
        self.add_url = reverse('add-to-purchases', kwargs={'pk': self.goods.pk})
        self.client.force_authenticate(user=self.user)

    def test_add_to_purchases(self):
        response = self.client.post(self.add_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.purchases.count(), 1)