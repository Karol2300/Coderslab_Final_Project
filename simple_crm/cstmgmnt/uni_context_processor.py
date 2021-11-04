from datetime import datetime
from django.http import request
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout


def application_info(request):
  ctx = {
    "application_name" : "simple crm",
    "now": datetime.now(),
    "version": "1.0",
    "copyrights": "Karol Zalecki",
    "contact": "karol@gkarol.com",
  }
  return ctx

def get_user_info(request):
  actual_user = request.user
  name = actual_user.username
  if actual_user.is_authenticated:
    ctx_2= {"username" : name}

  else:
    ctx_2 = {"username" : "Anonymus User"}
  return ctx_2


# def logout_login(request):
#   # if request.method == "GET":
#   #   actual_user = request.user
#   #   if actual_user.is_authenticated:
#   #     ctx_3 = {
#   #              "button_name": 'logout'
#   #              }
#   #
#   #   else:
#   #     ctx_3 = {
#   #            "button_name": 'login'}
#   #   return ctx_3
#
#   if request.method == "POST" and 'logout_login' in request.POST:
#     actual_user = request.user
#     if actual_user.is_authenticated:
#       logout(request)
#       return redirect('http://127.0.0.1:8000/loginPage')
#
#     else:
#       return redirect('http://127.0.0.1:8000/loginPage')