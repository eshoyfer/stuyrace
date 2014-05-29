from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from main.models import UserProfile, Event
from main.forms import EventCreationForm, EventReportForm, UserSettingsForm, UserRegistrationForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from urllib import quote

## Note:
## Django Convention wasn't followed (only because of discovering it at the end)
## Normally, when RequestContext is used, {{ user }} will refer to the logged in user in the templates
## But I didn't know about this 
## Correct way would've been: User (logged in) and Target
## I used: Viewer (logged in) and User (being viewed)
## So I did context['user'] to get the logged in user from context and re-assign it to viewer, my faulty name for it

def index(request):
	if request.user.is_authenticated():
		return logout_user(request)

	# Only come here on logout or upon entering the site
	# It's just a portal
	context = RequestContext(request)
	context_dict = {'messages': messages.get_messages(request)}
	return render_to_response('index.html', context_dict, context)

@login_required
def profile(request, ident=None):
	# ID by URL 
	# Viewer by cookie/session data

	# Need to pass: user, event_list, viewer
	context = RequestContext(request)
	viewer_object = context['user'] # See note above
	if ident is None:
		ident = viewer_object.id
	user_object = UserProfile.objects.get(id=ident)
	event_list = user_object.event
	context_dict = { 'user': user_object, 'event_list': event_list,'viewer': viewer_object, 'messages': messages.get_messages(request) }

	return render_to_response('profilepage.html', context_dict, context)

@login_required
def event(request, ident):
	# Event ID by URL
	# Viewer by cookie/session data
	context = RequestContext(request)

	viewer_object = context['user']
	event_object = Event.objects.get(id=ident)

	location1 = event_object.start #stringdata from db
	location2 = event_object.end #stringdata from db

	location1_enc = quote(location1)
	location2_enc = quote(location2)

	map_string = "http://maps.googleapis.com/maps/api/staticmap?size=300x200&markers=color:red%7Clabel:A%7C" + location1_enc + "&markers=color:blue%7Clabel:B%7C" + location2_enc

	loc1_string = "http://maps.googleapis.com/maps/api/streetview?size=300x200&location=" + location1_enc + "&fov=120&heading=60&pitch=10"
	loc2_string = "http://maps.googleapis.com/maps/api/streetview?size=300x200&location=" + location2_enc + "&fov=120&heading=60&pitch=10"
	context_dict = { 'event': event_object, 'viewer': viewer_object, 'messages': messages.get_messages(request), 'mapurl': map_string, 'loc1url': loc1_string, 'loc2url': loc2_string,
	 }

	return render_to_response('eventpage.html', context_dict, context)

@login_required
def friends(request):
	# Viewer by cookie/session data

	context = RequestContext(request)

	viewer_object = context['user']

	context_dict = { 'viewer': viewer_object, 'messages': messages.get_messages(request) }

	return render_to_response('friendslist.html', context_dict, context)

@login_required
def schedule(request):
	# Viewer by cookie/session data
	# Pass all events

	context = RequestContext(request)

	events = Event.objects.all()

	viewer_object = context['user']

	context_dict = { 'events': events, 'viewer': viewer_object, 'messages': messages.get_messages(request) }

	return render_to_response('scheduled.html', context_dict, context)

@login_required
def settings(request):
	# Viewer by cookie/session data

	context = RequestContext(request)

	viewer_object = context['user'] 

	# Logic 

	# Form submitted?
	if request.method == 'POST': 
		form = UserSettingsForm(request.POST, request.FILES, instance=viewer_object) # Form based on POST data, instance is viewer (editing viewer object)
		if form.is_valid(): # Validation
			viewer_form_model = form.save(commit=False)
			viewer_form_model.set_password(viewer_form_model.password)
			viewer_form_model.save()
			messages.add_message(request, messages.SUCCESS, 'Settings have been modified.')
		else: 
			messages.add_message(request, messages.ERROR, 'Something went wrong.')
			print form.errors
	else:
		form = UserSettingsForm(instance=viewer_object)

	context_dict = { 'viewer': viewer_object, 'form': form, 'messages': messages.get_messages(request)}

	return render_to_response('settings.html', context_dict, context)

@login_required
def results(request, ident):
	# Viewer by cookie/session data

	context = RequestContext(request)

	viewer_object = context['user']

	event_object = Event.objects.get(id=ident)

	# Logic 

	# Form submitted?
	if request.method == 'POST': 
		form = EventReportForm(request.POST, instance=event_object) # Form based on POST data, instance is viewer (editing viewer object)
		if form.is_valid(): # Validation
			form.save(commit=True) # Save changes
			messages.add_message(request, messages.SUCCESS, 'You have successfully submitted the results for the event!')

			return event(request, ident)
		else: 
			messages.add_message(request, messages.ERROR, "Check what you've done.")
			# Invalid
			print form.errors
	else:
		form = EventReportForm(request.POST, instance=event_object)
	
	context_dict = { 'viewer': viewer_object, 'form': form, 'event': event_object, 'messages': messages.get_messages(request) }
	return render_to_response('results.html', context_dict, context)

@login_required
def add(request, ident):
	# Viewer by cookie/session data

	context = RequestContext(request)

	viewer_object = context['user']

	user_object = UserProfile.objects.get(id=ident)

	viewer_object.friends.add(user_object)

	user_object.save()
	viewer_object.save()

	messages.add_message(request, messages.SUCCESS, 'You are now friends!')

	return profile(request, ident)

@login_required
def remove(request, ident):
	# Viewer by cookie/session data

	context = RequestContext(request)

	viewer_object = context['user']

	user_object = UserProfile.objects.get(id=ident)

	viewer_object.friends.remove(user_object)

	user_object.save()
	viewer_object.save()

	messages.add_message(request, messages.SUCCESS, 'You are no longer friends!')

	return profile(request, ident)

@login_required
def join(request, ident):
	# Viewer by cookie/session data

	context = RequestContext(request)

	viewer_object = context['user']

	event_object = Event.objects.get(id=ident)

	viewer_object.event.add(event_object)

	event_object.curr_players += 1

	viewer_object.save()
	event_object.save()

	messages.add_message(request, messages.SUCCESS, 'You have joined this event!')

	return event(request, ident)

@login_required
def leave(request, ident):
	# Viewer by cookie/session data

	context = RequestContext(request)

	viewer_object = context['user']

	event_object = Event.objects.get(id=ident)

	viewer_object.event.remove(event_object)

	event_object.curr_players -= 1

	viewer_object.save()
	event_object.save()

	messages.add_message(request, messages.SUCCESS, 'You have left this event!')

	return event(request, ident)

@login_required
def create(request):
	# Viewer by cookie/session data

	context = RequestContext(request)

	viewer_object = context['user']

	# Logic 

	# Form submitted?
	if request.method == 'POST': 
		form = EventCreationForm(request.POST) # Form based on POST data, new instance created
		if form.is_valid(): # Validation
			event_instance = form.save(commit=True) # Create new instance
			event_instance.save() # Save event to database
			messages.add_message(request, messages.SUCCESS, 'Event successfully created.')
			return event(request, event_instance.id) # Display created event page
		else: 
			messages.add_message(request, messages.ERROR, 'Something went wrong.')
			print form.errors
	else:
		form = EventCreationForm()

	context_dict = { 'viewer': viewer_object, 'form': form, 'messages': messages.get_messages(request)}

	return render_to_response('create.html', context_dict, context)

def register(request):
	# No data on viewer known
	context = RequestContext(request)
	# Logic 

	# This is a page that doesn't require you to be logged in.
	# If you are logged in, go through the logout_user procedure:
	# Get logged out, message is given, returned to index.
	if request.user.is_authenticated():
		return logout_user(request)

	# Form submitted?
	if request.method == 'POST': 
		form = UserRegistrationForm(request.POST) # Form based on POST data, new instance created
		if form.is_valid(): # Validation
			user_instance = form.save() # Create new instance
			user_instance.set_password(user_instance.password) # Password hash
			user_instance.save() # Save event to database
			messages.add_message(request, messages.SUCCESS, 'Registration successful!')
			# Take to login page 
			# For Login: return profile(request, user_instance.id)
			return HttpResponseRedirect('/main/login/')
		else: 
			messages.add_message(request, messages.ERROR, 'Something went wrong.')
			print form.errors
	else:
		form = UserRegistrationForm()

	context_dict = { 'form': form, 'messages': messages.get_messages(request), }

	return render_to_response('register.html', context_dict, context)

def login_user(request):
	# No data on viewer known

	# This is a page that doesn't require you to be logged in.
	# If you are logged in, go through the logout_user procedure:
	# Get logged out, message is given, returned to index.
	if request.user.is_authenticated():
		return logout_user(request)

	context = RequestContext(request)

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		# Authentication
		user_object = authenticate(username=username, password=password)

		if user_object: # Exists
			if user_object.is_active: # Active
				login(request, user_object) # Log them in
				# Redirection:
				return HttpResponseRedirect('/main/profile/')
			else:
				messages.add_message(request, messages.ERROR, 'Your Stuyrace account is disabled.')
		else: # Invalid user
			messages.add_message(request, messages.ERROR, 'Incorrect login info.')
		
	# Login form - GET
	form = UserLoginForm()


	context_dict = {'form': form, 'messages': messages.get_messages(request)}
	return render_to_response('login.html', context_dict, context)

@login_required
def logout_user(request):
	logout(request)
	messages.add_message(request, messages.SUCCESS, 'You have been logged out.')

	return HttpResponseRedirect('/main/') #Return to Index