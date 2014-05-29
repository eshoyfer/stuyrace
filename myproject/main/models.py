from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import F
import PIL

import datetime

class UserProfile(AbstractUser):
	created = models.DateTimeField(auto_now_add=True)
	friends = models.ManyToManyField('self') 
	leaderboard_status = models.BooleanField(default=True)
	picture = models.ImageField(upload_to="pictures", blank=True)

	def __unicode__(self):
		return self.get_username()

	# URL determined by default ID.

	def url(self):
		return "/main/profile/" + str(self.id)

	def link(self):
		# Username link HTML 
		return '<a href="/main/profile/' + str(self.id) + '">' + str(self) + "</a>"

	def add_url(self):
		return self.url() + "/add/"

	def remove_url(self):
		return self.url() + "/remove/"

	def default_picture_url(self):
		pass

class Event(models.Model):
	name = models.CharField(max_length=128)
	owner = models.ForeignKey(UserProfile, related_name='owned_event')
	participants = models.ManyToManyField(UserProfile, related_name = 'event')
	date = models.DateField()
	created = models.DateTimeField(auto_now_add=True)
	max_players = models.IntegerField()
	curr_players = models.IntegerField()
	public = models.BooleanField(default=True)
	completed = models.BooleanField(default=False)
	winner = models.ForeignKey(UserProfile, blank=True, null=True, related_name="won_event",) # UserProfile.objects.filter(event__id=event.id)
	start = models.CharField(max_length=128)
	end = models.CharField(max_length=128)
	# URL determined by default ID.

	def url(self):
		return "/main/event/" + str(self.id) + "/"

	def results_url(self):
		return "/main/results/" + str(self.id) + "/"

	def link(self):
		# Event name link HTML 
		return '<a href="/main/event/' + str(self.id) + '">' + str(self) + "</a>"

	def join_url(self):
		return self.url() + "join/"

	def leave_url(self):
		return self.url() + "leave/"

	def __unicode__(self):
		return self.name

