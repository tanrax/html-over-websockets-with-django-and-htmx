from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from tinymce import models as tinymce_models


class Profile(AbstractBaseUser):

    """User model"""

    email = models.EmailField("Email", unique=True)
    full_name = models.CharField(max_length=100, verbose_name="Full name", default="")
    avatar = models.ImageField(verbose_name="Avatar", upload_to="uploads/avatars/")

    USERNAME_FIELD = "email"  # make the user log in with the email

    def __str__(self):
        return self.email


class Category(models.Model):

    """Category model"""

    name = models.CharField(max_length=100, verbose_name="Nombre")

    class Meta:
        ordering = ("name",)
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.name


class Talk(models.Model):

    """Talk model"""

    title = models.CharField(max_length=100, verbose_name="Título")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="Categoría",
        verbose_name="Categoría",
    )
    author = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        related_name="author",
        verbose_name="Autor",
    )
    image = models.ImageField(verbose_name="Imagen", upload_to="uploads/talks/")
    is_draft = models.BooleanField(default=True, verbose_name="¿Es un borrador?")
    content = tinymce_models.HTMLField(verbose_name="Contenido")
    created_at = models.DateTimeField(auto_now=True, verbose_name="Creado")

    @property
    def slug(self):
        return slugify(self.title)

    @property
    def reading_time_min(self):
        # https://help.medium.com/hc/en-us/articles/214991667-Read-time
        READING_SPEED_OF_AN_ADULT = 265
        return ceil(
            len(strip_tags(self.content).split(" ")) / READING_SPEED_OF_AN_ADULT
        )

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Charla"
        verbose_name_plural = "Charlas"

    def __str__(self):
        return self.title
