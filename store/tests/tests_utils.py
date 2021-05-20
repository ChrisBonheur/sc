from django.test import TestCase
from django.core.cache import cache
from django.db.models import Q

from store.models import Article
from store.utils import get_or_create_cache

class UtilsTestCase(TestCase):
    def test_get_or_create_cache(self):
        get_or_create_cache(f"test_cache_tel", Article, Q(name__icontains="tel"))
        error_msg = "cache not create"
        self.assertNotEqual(cache.get("test_cache_tel", "not exist"), "not exist",\
            msg=error_msg)
        #assert exception if model name Error