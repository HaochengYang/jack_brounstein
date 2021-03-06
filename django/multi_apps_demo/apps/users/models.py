import re

from django.db import models
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
	def register(self, data):
		errors = []

		if not data["name"]:
			errors.append("Please enter a name")

		if not data["email"]:
			errors.append("Please enter an E-mail address")
		elif not EMAIL_REGEX.match(data["email"]):
			errors.append("Please enter a valid E-mail address")
		elif self.filter(email=data["email"]):
			errors.append("E-mail address in use")

		if not data["password"]:
			errors.append("Please enter a password")
		elif len(data["password"]) < 8:
			errors.append("Password must be at least 8 characters")
		elif data["password"] != data["confirm"]:
			errors.append("Passwords must match")

		response = {}

		if errors:
			response["added"] = False
			response["errors"] = errors
		else:
			response["added"] = True
			response["new_user"] = self.create(name=data["name"], email=data["email"], password=bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt()))

		return response

	def login(self, data):
		user = User.objects.filter(email=data["email"])

		if not user:
			return False
		else:
			user = user[0]

		pw = data["password"].encode()
		if bcrypt.hashpw(pw, user.password.encode()) == user.password.encode():
			return user
		else:
			return False

class User(models.Model):
	name = models.CharField(max_length=100)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = UserManager()