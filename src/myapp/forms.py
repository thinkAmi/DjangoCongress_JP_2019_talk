from django import forms


class ShinshuFruitForm(forms.Form):
    apple = forms.CharField(initial='Shinano Gold')
    grape = forms.CharField(initial='Shine Muscat')
    pear = forms.CharField(initial='Southern Suite')
