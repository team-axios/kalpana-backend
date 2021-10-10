from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import JsonResponse

from .models import Journal_Entry

import requests
import json
import uuid
import text2emotion as te

from .setup import SECRET_ACCESS_KEY, ACCESS_KEY

import boto3
session = boto3.Session(
	aws_access_key_id=ACCESS_KEY,
	aws_secret_access_key=SECRET_ACCESS_KEY
)

s3 = session.client('s3')

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
		generatedUUID = str(uuid.uuid4())
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

		response = requests.request("POST", "http://34.212.225.15:3000/notes/new/", headers=headers, data=payload)
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
		uud = dt["uuid"]
		model = Journal_Entry.objects.get(uid = uud)
		model.s3_path = 's3://kalpanageneratedaudios/' + uud + '.wav'
		model.save()
		return JsonResponse({
			"message": "New note added"
		}, status=201)
	else:
		return JsonResponse({
			"message": "Method not supported"
		}, status=400)

def generate_presigned_url(s3Path):
	uud = s3Path.replace("s3://kalpanageneratedaudios/", "")
	url = s3.generate_presigned_url(
		ClientMethod='get_object',
		Params={
			'Bucket': 'kalpanageneratedaudios',
			'Key': uud
		}
	)
	return url

def get_notes(request):
	li = []
	for i in Journal_Entry.objects.all():
		li.append({
			"title": i.title,
			"details": i.details,
			"url": generate_presigned_url(i.s3_path),
			"created_date": i.created_date
		})
	return JsonResponse({
		"message": li
	}, status=200)

