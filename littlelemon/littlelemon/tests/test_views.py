from django.test import TestCase
from restaurant.models import Menu
from restaurant.serializers import MenuSerializer
from django.contrib.auth.models import User
import json

TEST_CREDENTIALS = ['test', 'testing@123']

# unit test cases for the views here

class MenuItemsTest(TestCase):
    """
    Testing Strategy

    Test out all webpage views:
    > does the about page fetch?
    > does the book page fetch?
    > does the reservations page fetch?
    > does the menu page fetch?
    > does the single menu item page fetch?
    > does the bookings page fetch?

    Test out all the API endpoints:
    > does the tables perform CRUD?
    > does the menu items perform CRUD?
    """
    TOKEN = None
    
    def setUp(self) -> None:
        user_response = self.client.post('/auth/users/', data={
            'username': 'test',
            'password': 'testing@123',
            'email': 'test@littlelemon.com'
        })

        token = self.get_auth_token(*TEST_CREDENTIALS)

        response = self.client.post('/restaurant/menu/items/', headers={
            'Authorization': f'Token {token}',
        },
        data={
            'name': 'Ice Cream',
            'price': 80,
            'menu_item_description': 'Chilling delight for sweet lovers.',
            'inventory': 500
        })

    def get_auth_token(self, username, password):
        if self.TOKEN != None: return self.TOKEN

        response = self.client.post('/auth/token/login/', data={
            'password': password,
            'username': username
        })
        
        if response.status_code == 200: 
            self.TOKEN = response.json()['auth_token']
            return response.json()['auth_token']
        else: raise RuntimeError(f'{response.status_code}: query \'{username}/{password}\' retrieved no matching user.')
        
    def test_get_menu_all(self):
        token = self.get_auth_token(*TEST_CREDENTIALS)

        response = self.client.get('/restaurant/menu/items/', headers={
            'Authorization': f'Token {token}',
        })
        menu_items = response.json()

        all_menu_items = Menu.objects.all()
        all_menu_items_serialized = MenuSerializer(all_menu_items, many=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(menu_items, all_menu_items_serialized.data)

    def test_get_single_menu_item(self):
        token = self.get_auth_token(*TEST_CREDENTIALS)

        response = self.client.get('/restaurant/menu/items/2/', headers={
            'Authorization': f'Token {token}',
        })

        menu_item = Menu.objects.get(id=2)
        menu_item_serialized = MenuSerializer(menu_item)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), menu_item_serialized.data)

    def test_post_menu_item(self):
        token = self.get_auth_token(*TEST_CREDENTIALS)

        response = self.client.post('/restaurant/menu/items/', headers={
            'Authorization': f'Token {token}',
        },
        data={
            'name': 'Pasta',
            'price': 80,
            'menu_item_description': 'Italian delicacy for the taste savourers.',
            'inventory': 500
        })
        menu_item = response.json()

        single_menu_item = Menu.objects.get(id=menu_item['id'])
        single_menu_item_serialized = MenuSerializer(single_menu_item)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), single_menu_item_serialized.data)

        # other unit test cases ...

