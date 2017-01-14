from django import forms
from .models import UrlList

class UrlListForm(forms.ModelForm):

    class Meta:
        model = UrlList
        fields = ('target_urls', )
