from unittest import expectedFailure

from django.test import TestCase
from django.urls import reverse

from orders.models import Orders


class OrdersApiView_Test_Case(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.order_1 = Orders.objects.create(
            product_name='Laptop',
            quantity=10,
            customer_email='example@example.com'
        )
        cls.order_2 = Orders.objects.create(
            product_name='Phone',
            quantity=8,
            customer_email='example2@example2.com'
        )

    @classmethod
    def tearDownClass(cls):
        Orders.objects.all().delete()

    def setUp(self):
        self.data = {
            'product_name': 'Phone',
            'quantity': 8,
            'customer_email': 'example2@example2.com'
        }

    def test_get_all_orders(self):
        response = self.client.get(reverse('orders:orders-list'))
        response_data = response.json().get('results')
        status_order_1 = response_data[0].get('status')
        email = response_data[1].get('customer_email')

        self.assertEqual(len(response_data), 2)
        self.assertEqual(status_order_1, 'created')
        self.assertEqual(email, 'example2@example2.com')

    def test_one_order(self):
        current_order_pk = self.order_1.pk
        response = self.client.get(reverse('orders:orders-detail', kwargs={'pk': current_order_pk}))
        response_data = response.json()

        self.assertEqual(response_data.get('product_name'), self.order_1.product_name)
        self.assertEqual(response_data.get('quantity'), self.order_1.quantity)
        self.assertEqual(response_data.get('customer_email'), self.order_1.customer_email)

    def test_one_order_invalid_pk(self):
        current_order_pk = 12
        response = self.client.get(reverse('orders:orders-detail', kwargs={'pk': current_order_pk}))
        response_data = response.json()
        expected_response = 'No Orders matches the given query.'
        self.assertEqual(response_data.get('detail'), expected_response)

    def test_create_order(self):
        response = self.client.post(reverse('orders:orders-list'), data=self.data, content_type='application/json')
        response_data = response.json()

        self.assertEqual(response_data.get('product_name'), self.data.get('product_name'))
        self.assertEqual(response_data.get('quantity'), self.data.get('quantity'))
        self.assertEqual(response_data.get('customer_email'), self.data.get('customer_email'))

    def test_create_none_product_name_order(self):
        self.data['product_name'] = None
        response = self.client.post(reverse('orders:orders-list'), data=self.data, content_type='application/json')
        response_data = response.json()
        expected_response = ['This field may not be null.']

        self.assertEqual(response_data.get('product_name'), expected_response)

    def test_create_none_quantity_order(self):
        self.data['quantity'] = None
        response = self.client.post(reverse('orders:orders-list'), data=self.data, content_type='application/json')
        response_data = response.json()
        expected_response = ['This field may not be null.']

        self.assertEqual(response_data.get('quantity'), expected_response)

    def test_create_none_customer_email_order(self):
        self.data['customer_email'] = None
        response = self.client.post(reverse('orders:orders-list'), data=self.data, content_type='application/json')
        response_data = response.json()
        expected_response = ['This field may not be null.']

        self.assertEqual(response_data.get('customer_email'), expected_response)

    def test_create_invalid_product_name_order(self):
        self.data['product_name'] = ''
        response = self.client.post(reverse('orders:orders-list'), data=self.data, content_type='application/json')
        response_data = response.json()
        expected_response = ['This field may not be blank.']

        self.assertEqual(response_data.get('product_name'), expected_response)

    def test_create_invalid_quantity_order(self):
        self.data['quantity'] = 0
        response = self.client.post(reverse('orders:orders-list'), data=self.data, content_type='application/json')
        response_data = response.json()
        expected_response = ['This fields cannot be zero']

        self.assertEqual(response_data.get('quantity'), expected_response)

    def test_create_invalid_customer_email_order(self):
        self.data['customer_email'] = 'None'
        response = self.client.post(reverse('orders:orders-list'), data=self.data, content_type='application/json')
        response_data = response.json()
        expected_response = ['Enter a valid email address.']

        self.assertEqual(response_data.get('customer_email'), expected_response)

    def test_invalid_update_order(self):
        current_order_pk = self.order_1.pk
        response = self.client.patch(reverse('orders:orders-detail', kwargs={'pk': current_order_pk}),
                                     data={'status': 'wdqfga'}, content_type='application/json')
        response_data = response.json()
        expected_response = 'is not a valid choice.'

        self.assertIn(expected_response, response_data.get('status')[0])

    def test_update_order(self):
        current_order_pk = self.order_1.pk
        response = self.client.patch(reverse('orders:orders-detail', kwargs={'pk': current_order_pk}),
                                     data={'status': 'completed'}, content_type='application/json')
        response_data = response.json()
        expected_response = 'completed'

        self.assertEqual(expected_response, response_data.get('status'))
