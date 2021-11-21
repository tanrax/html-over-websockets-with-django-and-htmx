from app.website.models import Category, Talk, Profile
from faker import Faker

# Get random imagen from url
from django.core.files import File
import requests
import time
from tempfile import NamedTemporaryFile
from random import randint


def run():
    fake = Faker()

    # 100 talks
    for title in [fake.unique.sentence(nb_words=5)[0:-1] for i in range(100)]:
        my_talk = Talk(
            title=title,
            category=Category.objects.order_by("?")[0],
            speaker=Profile.objects.order_by("?")[0],
            is_draft=False,
            content=fake.paragraph(nb_sentences=randint(20, 100)),
        )
        my_talk.save()

        # Add a image
        url_random_imagen = f"https://cdn.jsdelivr.net/gh/tanrax/place-image-random/images/{randint(1, 1000)}.jpg"
        r = requests.get(url_random_imagen)
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(r.content)
        img_temp.flush()
        my_talk.image.save(f"random_{int(time.time() * 1000)}.jpg", File(img_temp))
