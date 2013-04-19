from django.db import models
# import Image
from PIL import Image
from photoupload.settings import STATIC_URL, MEDIA_ROOT
import os
from shutil import rmtree, copy2
 
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
 
## callable for upload_to ##
def upload_b_image(instance, filename):
    return os.path.join(str(instance.slug), 'b', filename)
     
class Photo(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField()
     
    b_image = models.ImageField(upload_to=upload_b_image)
    m_image = models.CharField(max_length=256, editable=False)
    s_image = models.CharField(max_length=256, editable=False)
    thumbnail = models.CharField(max_length=256, editable=False)
     
    def __unicode__(self):
        return self.title
     
    ## Create a Thumbnail column to show the thumbnail on the admin page 
    def admin_image(self):
        return "<img src='%s%s%s' />" % (STATIC_URL, '/photos/', self.thumbnail)
 
    admin_image.allow_tags = True
    admin_image.short_description = 'Thumbnail'
     
    ## override save function ##
    def save(self, *args, **kwargs):
     
        ## the location on the server where all the images will be saved into
        m_image_loc = os.path.join(MEDIA_ROOT, str(self.slug), 'm')
        s_image_loc = os.path.join(MEDIA_ROOT, str(self.slug), 's')
        t_image_loc = os.path.join(MEDIA_ROOT, str(self.slug), 't')
        b_image_loc = os.path.join(MEDIA_ROOT, str(self.slug), 'b', self.b_image.name)
         
        ## set the location based on the uploaded file 's name
        self.s_image = os.path.join(str(self.slug), 's', self.b_image.name)
        self.m_image = os.path.join(str(self.slug), 'm', self.b_image.name)
        self.thumbnail = os.path.join(str(self.slug), 't', self.b_image.name)
         
        image_name = ''
         
        ## check if this is saved at the first time, or is updated 
        temp_path_lst = self.b_image.name.rsplit(os.sep, 1)
         
        if len(temp_path_lst) == 1:
            ## if length equals to 1, then there is an image uploaded into the server, 
            ## in this case, delete all the old images
            image_name = self.b_image.name
            if os.path.exists(os.path.join(MEDIA_ROOT, str(self.slug))):
                rmtree(os.path.join(MEDIA_ROOT, str(self.slug)))
        else:
            ## if image is still the same, then just save the other properties 
            ## and exit the function
            image_name = temp_path_lst[1]
            super(Photo, self).save()
            return
     
        super(Photo, self).save()
         
        ## create all the folders containing images
        if not os.path.exists(m_image_loc):
            os.makedirs(m_image_loc)
             
        if not os.path.exists(s_image_loc):
            os.makedirs(s_image_loc)
             
        if not os.path.exists(t_image_loc):
            os.makedirs(t_image_loc)
             
        ## copy the uploaded images into small-size folder, medium-size folder 
        ## and thumbnail folder
        copy2(b_image_loc, m_image_loc)
        copy2(b_image_loc, s_image_loc)
        copy2(b_image_loc, t_image_loc)
 
        ## resize all the images
        ## medium size
        image = Image.open(os.path.join(m_image_loc, image_name))
        width, height = image.size
        size = width / 2, height / 2
        image = image.resize(size, Image.ANTIALIAS)
        image.save(os.path.join(m_image_loc, image_name))
         
        ## small size
        image = Image.open(os.path.join(s_image_loc, image_name))
        width, height = image.size
        size = width / 4, height / 4
        image = image.resize(size, Image.ANTIALIAS)
        image.save(os.path.join(s_image_loc, image_name))
         
        ## thumbnail 
        image = Image.open(os.path.join(t_image_loc, image_name))
        width, height = image.size
        size = width / 10, height / 10
        image = image.resize(size, Image.ANTIALIAS)
        image.save(os.path.join(t_image_loc, image_name))
         
## cleaning up function ## 
@receiver(post_delete, sender=Photo)
def _photo_del(sender, instance, **kwargs):
    if instance.slug:
        rmtree(os.path.join(MEDIA_ROOT, str(instance.slug)))
