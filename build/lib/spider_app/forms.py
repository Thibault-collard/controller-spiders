from django import forms
from django.core.validators import RegexValidator



numeric = RegexValidator(r'^[0-9+]', 'Only digit characters.')

class NameForm(forms.Form):
    
    CHOICES=[("MJ",'MJ'),
        ("PP",'PP'),
        ("Prod",'Prod'),
        ("Test",'Test'),
        ("Awin_pub","Awin_pub"),
        ("Prospection_apollo_12012022","Prospection_apollo_12012022")
        ]

    result_max = brand_max = network_max = start_row = end_row = forms.CharField(required=True, error_messages = {'required':"Please Enter a valid numeric value"}, validators=[numeric])
    spider_name = mode = name_spread = forms.ChoiceField(choices=CHOICES,required=True)

