# coding: utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

from ..controllers import user as controllers
from codeshipper_app.models.server import Server
from codeshipper_app.models.project import Project
from codeshipper_app.models.role import Role
import json, pytz

def left_menu_user(request):
	user = request.user
	if not user.id:
		return redirect("/accounts/login/")

	users = User.objects.filter()
	context = {
		"list_data": users
	}
	content_type = "application/html"
	template_name = "pages/user_list.html"
	return HttpResponse(render(request, template_name, context=context, content_type=content_type))


def get_list_server(user):
	if user.is_superuser:
		return Server.objects.filter()


def get_list_project(user):
	if user.is_superuser:
		return Project.objects.filter()


def get_list_role(user):
	ld = []
	lr = Role.objects.filter(user=user)
	
	if len(lr):
		for item in lr:
			ld.append(model_to_dict(item))
	return ld

def user_detail(request, user_id):
	request_user = request.user
	if not request_user.id:
		return redirect("/accounts/login/")

	user = User.objects.filter(id=user_id).first()
	if user:
		user_dict = model_to_dict(user)
	else:
		user_dict = None
	
	def make_sugestion_server(li):
		ld = []
		for item in li:
			item_dict = {
				"id": f"{item.id}",
				"host": f"{item.name}:{item.port}"
			}
			ld.append(item_dict)
		return ld

	def make_sugestion_project(li):
		ld = []
		for item in li:
			item_dict = {
				"id": f"{item.id}",
				"name": f"{item.name}"
			}
			ld.append(item_dict)
		return ld

	list_servers = make_sugestion_server(get_list_server(request_user))

	list_projects = make_sugestion_project(get_list_project(request_user))

	list_roles = get_list_role(user)
	
	context = {
		"item": user_dict,
		"list_servers": list_servers,
		"list_projects": list_projects,
		"list_roles": list_roles,
	}
	context["cs_data"] = context.copy()

	content_type = "application/html"
	template_name = "pages/user_detail.html"
	return HttpResponse(render(request, template_name, context=context, content_type=content_type))
