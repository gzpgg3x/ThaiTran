## forms.py
class PhotoAdminForm(ModelForm):
    b_image = FileField(widget=AdminImageFieldWidget)
     
    class Meta:
        model = Photo
         
