from django.core.cache import cache
from django.shortcuts import reverse
from PIL import Image
import logging as lg

def add_percentage(price_init):
    PERCENTAGE_15 = 15
    PERCENTAGE_10 = 10
    LIMIT_MOUNT = 15000
    
    if price_init > LIMIT_MOUNT:
        percentage_getted = (PERCENTAGE_10 * price_init) / 100
    elif price_init <= LIMIT_MOUNT:
        percentage_getted = (PERCENTAGE_15 * price_init) / 100
    
    return percentage_getted + price_init

def edit_image_before_save(path_file, width_min):
    """This ffunction resize image before save"""
    img = Image.open(path_file)
    img = img.convert('RGB')
    
    if img.width > width_min:
        img_height = img.height
        #get width image are depressed and we depressed this value from 
        #initial image height
        percentage_remove_px = (100 * (img.width - width_min)) / img.width#percentage of removing px
        output_height = (percentage_remove_px * img_height) / 100#get px to remove in height
        output_height = img_height - output_height#remove height 
        output_height = int(output_height)#convert height to integer
        
        output_size = (width_min, output_height)
        img.thumbnail(output_size)
        
        #save output image
        img.save(path_file)
        
def send_welcome_message_to_new_user(user, NotifMessage, User):
    try:
        User.objects.get(pk=user.id)
    except:
        #no login user
        return False
    else:
        content = f'Bienvenue {user}, sur notre plate-forme de vente en ligne SC! \
                Si vous voyez ce message c\'est que votre compte a bien été crée, nous vous\
                    prions de bien vouloir completer vos informations de profil en cliquant \
                        sur ce message !'
        
        #Verification if user has welcome message or no(if no: creating for welcome msg)            
        message = NotifMessage.objects.filter(user=user, content=content)
        #If user has no notif, that's mean user is newcomer 
        if not message:
            NotifMessage.objects.create(
                content=content,
                user=user,
                link=reverse('user:profil')
            )
        return True

#=====================================================================================
#showing messages info
article_update_success = lambda article: f"Votre article {article} a été modifié!"
article_save_success = lambda article: f"Votre article {article} a bien été ajouté !"
article_delete_success = lambda article: f"Votre article {article} a été supprimé !"
article_add_in_favourite_success = lambda article: f"l'article {article} a été ajouté aux favoris !"
article_add_in_favourite_if_exist = lambda article: f"l'article {article} existe déjà aux favoris !"
#======================================================================================

def get_or_create_cache(cache_name, model, Q_object=None):
    """get or create cache if not exist for model filter
    Args:
        cache_name (str): name of cache
        model (model class): model to filter
        Q_object: filter model with Q object from django.db.models 
    """
    if cache.get(cache_name, "not exist") == "not exist":
        try:
            if Q_object != None:
                cache.set(cache_name, model.objects.filter(Q_object))
            else:
                cache.set(cache_name, model.objects.all())
        except NameError as e:
            lg.critical(f"Model name not found : {e}")
        except Exception as e:
            lg.warning(e)
    
    return cache.get(cache_name, "not exist")


def resize_proportion_image(image_path, image_size=(263, 350)):
    """Redefine proportion of an image by percentage with base
    percentage 75/100 
    Args: 
        image_size (tuple): the size proportion of an image 
    """
    width=75
    height=100
    image = Image.open(image_path)
    initial_width_px = image.width
    initial_height_px = image.height
    #get percentage of image width 
    image_percentage_width = (initial_width_px * height) / image.height
    #verify if image_percentage_width is great than default width dismiss width px:
    if image_percentage_width > width:
        new_width_px = image_size[0]
        new_height_px = (new_width_px * initial_height_px) / initial_width_px
        new_size = (new_width_px, int(new_height_px))
        image.thumbnail(new_size)
        #save output image
        image.save(image_path)
    #if with percentage is lower than default width center, dismiss height percentage 
    elif image_percentage_width < width:
        print("yes")
        #get proportion percentage about height
        percentage_width_missing = width - image_percentage_width 
        new_height_percentage = height - percentage_width_missing# now proportion is 100 / 75
        new_height_px = (new_height_percentage * initial_height_px) / 100
        #crop image in center
        px_remove_from_initial_height = initial_height_px - new_height_px
        image.crop((0, px_remove_from_initial_height / 2, initial_width_px, new_height_px))\
            .resize(image_size).save(image_path)
        