from django.test import TestCase
from django.core.cache import cache
from django.db.models import Q
from django.conf import settings
from store.models import Article
from store.utils import get_or_create_cache, resize_proportion_image
from PIL import Image
from os import system

class UtilsTestCase(TestCase):
    def test_get_or_create_cache(self):
        get_or_create_cache(f"test_cache_tel", Article, Q(name__icontains="tel"))
        error_msg = "cache not create"
        self.assertNotEqual(cache.get("test_cache_tel", "not exist"), "not exist",\
            msg=error_msg)
        #assert exception if model name Error
        
    def test_resize_proportion_image(self):
        image_path = f"{settings.BASE_DIR}/store/static/store/img_test/huit.jpg"
        #creating a copy of file that will be distroyed after test
        system(f"cp {image_path} {settings.BASE_DIR}/store/static/store/img_test/pic5_test.png")        
        image_path = f"{settings.BASE_DIR}/store/static/store/img_test/pic5_test.png"
        image = Image.open(image_path)
        initial_width = image.width
        resize_proportion_image(image_path)
        image = Image.open(image_path)
        #delete copy file image
        system(f"rm {image_path}")
        
        self.assertNotEqual(image.width, initial_width)