import datetime

from django.conf import settings
from django.db import models
from django.db.utils import IntegrityError
from django.utils import timezone


# limit links and categories returned to only those owned by the logged in user;
# requires an extra "user" arg
class UserManager(models.Manager):
    def all(self, user):
        return super().all().filter(user=user)


class Category(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    objects = UserManager()

    class Meta:
        ordering = ['name']
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Link(models.Model):
    url = models.CharField(max_length=4096)
    note = models.CharField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    objects = UserManager()

    class Meta:
        ordering = ['category', '-updated']

    def save(self, *args, **kwargs):
        # if no user is given don't fail here; instead let normal integrity check catch it
        if hasattr(self, 'user') and self.user != self.category.user:
            raise IntegrityError("Link user must match category user")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.url


class UserPref(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    theme = models.CharField(max_length=2, choices=settings.THEME_CHOICES_TUPLES, default=settings.THEME_DEFAULT)

    def __str__(self):
        return "{} theme {}".format(self.user.username, self.theme)
