from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class UserRegistrationForm(UserCreationForm):
	email = forms.EmailField()
	
	class Meta:
		model = User
		fields = ['username','email','password1','password2']
		
class InputForm(forms.Form):
  Date = forms.DateField(label="Date: yyyy-mm-dd")
  CID = forms.CharField(max_length=7)
  Code = forms.CharField(max_length=10)
  Attended = forms.CharField(max_length=3, label="Attended? ( YES, NO, N/A)")
  
class DeleteForm(forms.Form):
	userName = forms.CharField()
