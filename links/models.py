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

    def __str__(self):
        return self.name


class Link(models.Model):
    url = models.CharField(max_length=4096)
    note = models.CharField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    objects = UserManager()

    class Meta:
        ordering = ['category', '-updated']
        """
        constraints = [
            models.CheckConstraint(
                check=models.Q(user = models.F("category__user")),
                name='user_constraint',
            ),
        ]
        """

    def save(self, *args, **kwargs):
        if hasattr(self, 'user') and self.user != self.category.user:
            raise IntegrityError("Link user must match category user")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.url
