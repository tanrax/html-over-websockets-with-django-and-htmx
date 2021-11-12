from django.shortcuts import render
from django.template.loader import render_to_string
from random import randint
from django.conf import settings
from .models import Talk
from asgiref.sync import sync_to_async


def index(request):
    """Render layout page"""
    return render(request, "layouts/base.html", {
        "room_random": randint(1000000, 9999999),
        "DOMAIN": settings.DOMAIN,
    })

def page_talks():
    return render_to_string("pages/talks.html", {
        "talks": Talk.objects.order_by("title")[:5]
    })


def page_about():
    return render_to_string("pages/about.html", {})