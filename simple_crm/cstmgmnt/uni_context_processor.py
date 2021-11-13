from datetime import datetime
from django.http import request
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.views import View


def application_info(request):
    ctx = {
        "application_name": "simple crm",
        "version": "1.0",
        "copyrights": "Karol Zalecki",
        "contact": "karol@gkarol.com",
    }
    return ctx


def get_user_info(request):
    actual_user = request.user
    name = actual_user.username
    if actual_user.is_authenticated:
        ctx_2 = {"username": name}

    else:
        ctx_2 = {"username": "Anonymus User"}
    return ctx_2
