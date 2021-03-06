from django.shortcuts import render, redirect
from .models import Course
from ..users.models import User

def index(request):
	if "user_id" not in request.session:
		return redirect("users:login_page")

	context = {
		"courses": Course.objects.all(),
	}
	return render(request, "courses/index.html", context)

def new(request):
	return render(request, "courses/new.html")

def create(request):
	Course.objects.create(name=request.POST["name"], description=request.POST["description"])
	return redirect("courses:index")

def add_student_page(request):
	context = {
		"courses": Course.objects.all(),
		"students": User.objects.all(),
	}
	return render(request, "courses/add_student_to_course.html", context)

def add_student_to_course(request):
	course = Course.objects.get(id=request.POST["course_id"])
	student = User.objects.get(id=request.POST["user_id"])

	course.users.add(student)

	return redirect("courses:add_student_page")

def show(request, course_id):
	context = {
		"course": Course.objects.get(id=course_id),
	}
	return render(request, "courses/show.html", context)

def destroy(request):
	Course.objects.get(id=request.POST["course_id"]).delete()
	return redirect("courses:index")