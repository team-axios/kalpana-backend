from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import JsonResponse

from .models import Journal_Entry

import requests
import json
import uuid
import text2emotion as te

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
		# predict tone of text here
		tone = te.get_emotion(details)
		# print(tone)
		# [happy, angry, fear, surprise, sad]
		# happy, surprise | angry | fear, sad
		# set tempo 0.5 for happy, surprise | set tempo for 0.33 for angry | set tempo for 0.25 for fear, sad
		selectedTone = None
		selectedScore = -0.25
		for i in tone.keys():
			if tone[i] > selectedScore:
				selectedScore = tone[i]
				selectedTone = i
		generatedUUID = uuid.uuid4()
		entry = Journal_Entry.objects.create(
			title = title,
			details = details,
			uid = generatedUUID,
			s3_path = '',
			tone = selectedTone
		)
		payload = json.dumps({
			"details": details,
			"tone": selectedTone,
			"uuid": generatedUUID
		})
		headers = {
			'Content-Type': 'application/json'
		}

		response = requests.request("POST", url, headers=headers, data=payload)
		return JsonResponse({
			"message": "New note added"
		}, status=201)
	else:
		return JsonResponse({
			"message": "Method not supported"
		}, status=400)

def update_note(request):
	if request.method == 'POST':
		dt = json.loads(request.body)
		uuid = dt["uuid"]
		print(dt["message"])
		model = Journal_Entry.objects.filter(uid = uuid)[0]
		model.s3_path = 's3://kalpanageneratedaudios/' + uuid.mid
		model.save()
		return JsonResponse({
			"message": "New note added"
		}, status=201)
	else:
		return JsonResponse({
			"message": "Method not supported"
		}, status=400)