from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe
import Image
import os
from photoupload.settings import MEDIA_ROOT, STATIC_URL
 
class AdminImageFieldWidget(AdminFileWidget):
    def render(self, name, value, attrs=None):
        output = []
        file_name = str(value)
         
        if file_name:
            file_path = os.path.join(MEDIA_ROOT, file_name)
            ## file_name contains the path to the big image. I want to show 
            ## the small image on the update form, so I will replace the 'b' 
            ## folder with the 's' folder
            file_name = file_name.replace(os.sep + 'b' + os.sep, os.sep + 's' + os.sep, 1)
             
            try:
                image = Image.open(file_path)
                output.append("<img src='%s%s%s' />" %(STATIC_URL, '/photos/', file_name))
                 
            except IOError:
                output.append('<b>There is no image </b>')
 
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
         
        return mark_safe(u''.join(output))