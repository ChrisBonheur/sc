from django.test import TestCase
from django.core.files import File
from os import system

from .tests_views import create_article
from store.models import Picture

class SignalsTestCase(TestCase):
    def setUp(self):
        self.article = create_article()
        
    def test_rm_picture_signal(self):
        """test image is deleted from server after removing article"""
        article = self.article
        img = File(open(article.image_min.path, 'rb'))
        Picture.objects.create(photo=img, article=article)
        imgs = Picture.objects.filter(article=article)
        article.delete()
        for img in imgs:
            #for each picture of article try to find it
            find_file = system(f'find {img.photo.path}  2> /dev/null')
            self.assertNotEqual(find_file, 0, msg="File not remove")
        find_file = system(f'find {article.image_min.path} 2> /dev/null')
        self.assertNotEqual(find_file, 0, msg="File not remove")
    
        
