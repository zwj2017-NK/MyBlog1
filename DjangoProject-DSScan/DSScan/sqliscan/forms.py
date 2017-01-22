from django import forms
from .models import UrlList, ScanConfig

class UrlListForm(forms.ModelForm):

    class Meta:
        model = UrlList
        fields = ('target_urls', )


class SearchForm(forms.Form):
    query = forms.CharField()


class ScanConfigForm(forms.ModelForm):

    class Meta:
        model = ScanConfig
        fields = ('thread_num', )