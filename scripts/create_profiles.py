from app.website.models import Profile
from faker import Faker

# Get random imagen from url
from django.core.files import File
import requests
import time
from tempfile import NamedTemporaryFile
from random import randint


def run():
    fake = Faker()

    # 30 Profiles random
    for email in [fake.unique.email() for i in range(30)]:
        my_profile = Profile()
        my_profile.email = email
        my_profile.full_name = f"{fake.first_name()} {fake.last_name()}"
        my_profile.set_password("password")
        my_profile.save()
        # Add a profile picture
        url_random_imagen = f"https://cdn.jsdelivr.net/gh/tanrax/place-image-random/images/{randint(1, 1000)}.jpg"
        r = requests.get(url_random_imagen)
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(r.content)
        img_temp.flush()
        my_profile.avatar.save(f"random_{int(time.time() * 1000)}.jpg", File(img_temp))
