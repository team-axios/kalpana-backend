from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import JsonResponse

from .models import Journal_Entry

import json
import uuid

# Create your views here.
def login_user_api(request):
	if request.method == 'POST':
		dt = json.loads(request.body)
		username = dt["username"]
		password = dt["password"]
		user = authenticate(request, username=username, password=password)
		if user is None:
			return JsonResponse({
				"message": "An error occurred"
			}, status=401)
		else:
			return JsonResponse({
				"message": "Login successful"
			}, status=200)
	else:
		return JsonResponse({
			"message": "Method not supported"
		}, status=400)

def register_user_api(request):
	if request.method == 'POST':
		dt = json.loads(request.body)
		username = dt["username"]
		email = dt['email']
		password = dt['password']
		user = User.objects.filter(username=username)
		if len(user) == 0:
			user = User.objects.create_user(username, email, password)
			return JsonResponse({
				"message": "Registration successful"
			}, status=200)
		else:
			return JsonResponse({
				"message": "User already exists"
			}, status=401)
	else:
		return JsonResponse({
			"message": "Method not supported"
		}, status=400)

def create_new_note(request):
	if request.method == 'POST':
		dt = json.loads(request.body)
		title = dt["title"]
		details = dt["note"]
		entry = Journal_Entry.objects.create(
			title = title,
			details = details,
			uid = uuid.uuid4(),
			s3_path = '',
			tone = ''
		)
		return JsonResponse({
			"message": "New note added"
		}, status=201)
	else:
		return JsonResponse({
			"message": "Method not supported"
		}, status=400)