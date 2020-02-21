from django.forms import ModelForm
from .models import *

class NewModelForm(ModelForm):
    class Meta:
        model = NewModel
        exclude = []
        fields = "__all__"
