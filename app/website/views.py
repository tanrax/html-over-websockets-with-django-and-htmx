from django.shortcuts import render
from django.template.loader import render_to_string
from random import randint
from django.conf import settings
from .models import Talk, Profile
from asgiref.sync import sync_to_async


def index(request):
    """Render layout page"""
    return render(
        request,
        "layouts/base.html",
        {
            "room_random": randint(1000000, 9999999),
            "DOMAIN": settings.DOMAIN,
        },
    )


def page_talks(page=1):
    TALK_PER_PAGE = 5
    START = TALK_PER_PAGE * (page - 1)
    END = TALK_PER_PAGE * page
    return render_to_string(
        "pages/talks.html",
        {
            "talks": Talk.objects.order_by("title")[START:END],
            "page": page,
            "next_page": page + 1,
        },
    )


def page_single_talk(id):
    return render_to_string(
        "pages/talk-single.html",
        {
            "talk": Talk.objects.get(id=id),
        },
    )

def page_profiles():
    return render_to_string(
        "pages/profiles.html",
        {
            "profiles": Profile.objects.order_by("full_name"),
        },
    )



def page_about():
    return render_to_string("pages/about.html", {})


def page_results(search):
    return render_to_string(
        "pages/talks.html",
        {
            "talks": Talk.objects.filter(
                title__icontains=search.lower()
                                         ).order_by("title"),
            "search": search,
        },
    )
