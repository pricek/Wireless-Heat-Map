from django import forms
import datetime

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)

class DateInput(forms.DateInput):
    input_type = 'date'

class DateForm(forms.Form):
    select_date = forms.DateField(label='Date to view', widget=DateInput(attrs={'max' : datetime.date.today()}), initial=datetime.date.today)