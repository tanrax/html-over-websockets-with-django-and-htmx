from app.website.models import Category
from faker import Faker

def run():
    fake = Faker()

    # 5 categories
    for word in [fake.unique.sentence(nb_words=1)[0:-1] for i in range(5)]:
        Category(name=word).save()