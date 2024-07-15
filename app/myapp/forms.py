#forms.py

from django import forms
from .models import ImagePair
from django.conf import settings

class ImagePairForm(forms.ModelForm):

    template = forms.ChoiceField(choices=settings.TEMPLATES_OPTIONS, label='Choose Template')
    class Meta:
        model = ImagePair
        #BLUE -  
        # fields = ['image1', 'image2']
        fields = ['image1', 'image2', 'template']