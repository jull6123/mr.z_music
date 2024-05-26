import os

from django.http import FileResponse
from django.shortcuts import render, HttpResponse, redirect
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
import hashlib
from django.shortcuts import render
from urllib.parse import unquote

from demoone import models


from django import forms

from django.conf import settings


def app(request):
    return render(request, "View/App.view")


def playing(request):
    return render(request, "View/Playing.view")