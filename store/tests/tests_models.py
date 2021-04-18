from django.test import TestCase
from django.core.files import File
from os import system

from .tests_views import create_article
from store.models import Picture

class SignalsTestCase(TestCase):
    def test_rm_picture_signal(self):
        """test image is deleted from server after removing article"""
        article = create_article()
        img = File(open(article.image_min.path, 'rb'))
        Picture.objects.create(photo=img, article=article)
        imgs = Picture.objects.filter(article=article)
        article.delete()
        for img in imgs:
            #for each picture of article try to find it
            find_file = system(f'find {img.photo.path}')
            self.assertNotEqual(find_file, 0)
        find_file = system(f'find {article.image_min.path}')
        self.assertNotEqual(find_file, 0)
        
