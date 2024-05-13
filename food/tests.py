from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from django.test import TestCase
from food.models import Item


class ItemModelTest(TestCase):
    def test_item_creation(self):
        item = Item.objects.create(
            item_name="Test Item",
            item_desc="Test Description",
            item_price=10,
            views=0
        )
        self.assertEqual(item.item_name, "Test Item")
        self.assertEqual(item.item_desc, "Test Description")
        self.assertEqual(item.item_price, 10)
        self.assertEqual(item.views, 0)


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
