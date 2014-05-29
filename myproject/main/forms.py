from django import forms
from main.models import UserProfile, Event
from django.contrib.auth.models import User

# You could declare a field normally in forms.py but in your templates html file use {{ form.field.as_hidden }}

class EventCreationForm(forms.ModelForm):
	owner = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset=UserProfile.objects.all())
	curr_players = forms.IntegerField(widget=forms.HiddenInput(), initial=1)
	# Create event
	class Meta:
		
		model = Event
		fields = ('name', 'start', 'end', 'curr_players', 'max_players', 'date', 'owner', 'public',)

class EventReportForm(forms.ModelForm):
	# Report result of event
	completed = forms.BooleanField(widget=forms.HiddenInput(), initial=True)

	class Meta:
		model = Event
		fields = ('winner', 'completed')

class UserSettingsForm(forms.ModelForm):
	# Changing settings

	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = UserProfile
		fields = ('first_name', 'last_name', 'email', 'password', 'leaderboard_status', 'picture')

class UserRegistrationForm(forms.ModelForm):
	# Registration
	
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = UserProfile
		fields = ('first_name', 'last_name', 'email', 'username',  'password')

class UserLoginForm(forms.ModelForm):
	# Login

	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = UserProfile
		fields = ('username', 'password',)
