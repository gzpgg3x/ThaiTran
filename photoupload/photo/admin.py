## admin.py
import models
from django.contrib import admin
from django.contrib.auth.models import User
from photo.models import Photo

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'admin_image')
    prepopulated_fields = {'slug':('title',)}
     
    # form = PhotoAdminForm
     
admin.site.register(Photo, PhotoAdmin)