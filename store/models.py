from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.utils import timezone
from os import system, path
from PIL import Image


from user.models import Profil
from .utils import edit_image_before_save, add_percentage 

def pictures_rename(instance, filename):
    upload_to='article_img'
    ext = filename.split('.')[-1]
    if instance.pk:
        filename = f'{instance.pk}.{ext}'
    else:
        try:
            last_id = Article.objects.last().id
        except:
            last_id = 1 
        new_name = f'img{last_id}'
        filename = f'{new_name}.{ext}'
    
    return path.join('uploads', filename)

def path_and_rename(instance, filename):
    upload_to='article_img'
    ext = filename.split('.')[-1]
    if instance.pk:
        filename = f'{instance.pk}.{ext}'
    else:
        try:
            last_id = Article.objects.last().id
        except:
            last_id = 1 
        new_name = f'img{last_id}'
        filename = f'{new_name}.{ext}'
    
    return os.path.join('uploads', filename)

class Identity(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=True)
    def __str__(self):
        return self.name
    class Meta:
        abstract = True
    
class Category(Identity):
    class Meta:
        verbose_name = 'Categorie'

class Status(Identity):
    class Meta:
        verbose_name = "Etat"

class Town(Identity):
    class Meta:
        verbose_name = "Villes"

class Article(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nom de l\'article')
    description = models.TextField()
    price_init = models.IntegerField(verbose_name='Prix initial', null=True)
    price_ttc = models.IntegerField(verbose_name='Prix TTC', null=True)
    number = models.IntegerField(verbose_name='Nombre d\'article dispo', default=1)
    available = models.BooleanField(verbose_name='Disponible', default=True)
    district = models.CharField(max_length=100, verbose_name='Quartier')
    seen = models.IntegerField(verbose_name='Nombre de vue', default=0)
    date_add = models.DateTimeField(auto_now_add=True, verbose_name='Ajouté')
    date_edit = models.DateTimeField(auto_now_add=False, verbose_name='Modifié', null=True)
    image_min = models.ImageField(upload_to=pictures_rename, null=True)
    img_background = models.CharField(max_length=100, null=True)
    delivery = models.BooleanField(default=False, null=True)
    slug = models.SlugField(max_length=100, blank=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name='Etat', null=True)
    town = models.ForeignKey(Town,on_delete=models.CASCADE, verbose_name='Ville', null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name='Categorie',\
        null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Utilisateur')
    
    class Meta:
        verbose_name = 'Article'
        ordering = ['-date_add']
        
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.price_ttc = add_percentage(self.price_init)
        self.date_edit = timezone.now()
        if self.number == 0:
            self.available = False
        super().save(*args, **kwargs)
        edit_image_before_save(self.image_min.path, 255)
        
class Picture(models.Model):
    photo = models.ImageField(upload_to=pictures_rename, null=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        edit_image_before_save(self.photo.path, 400)

class SocialApp(Identity):
    class Meta:
        verbose_name = "Applications sociales de partage"

class Share(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    social_app = models.ForeignKey(SocialApp, on_delete=models.CASCADE)
    date_share = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Partage sur réseaux sociaux"
    
class Favourite(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    articles = models.ManyToManyField(Article, related_name="favourite")

    class Meta:
        verbose_name = 'Favoris'

@receiver(post_delete, sender=Article)
def rm_picture_signal(sender, instance, **kwargs):
    """Remove article pictures from server when article deleted"""
    photo_min = instance.image_min
    system(f'rm {photo_min.path} 2> /dev/null')
    article_pictures = Picture.objects.filter(article=instance)
    for pic in article_pictures:
        try:
            system(f'rm {pic.photo.path} 2> /dev/null')
        except:
            print("Can't delete file")
