# здесь буду прописывать формы

from django import forms


class SendMessageForm(forms.Form):
    user_id = forms.IntegerField()
    message = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))