from PIL import Image

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
        
def send_welcome_message_to_new_user(user, Message, User):
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
        message = Message.objects.filter(recipient_id=user.id, content=content)
        #If user has no notif, that's mean user is newcomer 
        if not message:
            Message.objects.create(
                content=content,
                recipient_id=user.id,
                type_msg='notif',
                link='user:profil'
            )
        return True

#showing message 
article_update_success = lambda article: f"Votre article {article} a été modifié!"