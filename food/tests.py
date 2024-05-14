from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
# from selenium import webdriver
from django.test import TestCase
from food.models import Item


# class ItemModelTest(TestCase):
#     def test_item_creation(self):
#         item = Item.objects.create(
#             item_name="Test Item",
#             item_desc="Test Description",
#             item_price=10,
#             views=0
#         )
#         self.assertEqual(item.item_name, "Test Item")
#         self.assertEqual(item.item_desc, "Test Description")
#         self.assertEqual(item.item_price, 10)
#         self.assertEqual(item.views, 0)


# class StaticFilesTest(StaticLiveServerTestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.browser = webdriver.Chrome()
#
#     @classmethod
#     def tearDownClass(cls):
#         cls.browser.quit()
#         super().tearDownClass()
#
#     def test_static_files(self):
#         self.browser.get(self.live_server_url + '/static/food/style.css')
#         self.assertIn('food', self.browser.page_source)


class ItemDeleteTestCase(TestCase):
    def setUp(self):
        # Create some items for testing
        self.item1 = Item.objects.create(item_name='Item 1', item_desc='Description 1')
        self.item2 = Item.objects.create(item_name='Item 2', item_desc='Description 2')

    def test_delete_item(self):
        # Get the URL for deleting an item
        delete_url = reverse('food:delete_item', args=[self.item1.id])

        # Check if the item exists before deletion
        self.assertTrue(Item.objects.filter(item_name='Item 1').exists())

        # Send a DELETE request to delete the item
        response = self.client.delete(delete_url)

        # Check if the item is deleted
        self.assertFalse(Item.objects.filter(item_name='Item 1').exists())

        # Check if the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)

    def test_delete_nonexistent_item(self):
        # Get the URL for deleting an item that doesn't exist
        delete_url = reverse('food:delete_item', args=[9999])

        # Send a DELETE request to delete the item
        response = self.client.delete(delete_url)

        # Check if the response status code is 404 (not found)
        self.assertEqual(response.status_code, 404)