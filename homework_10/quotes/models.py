from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    fullname = models.CharField(max_length=50)
    born_date = models.DateField(default="2024-02-02")
    born_location = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.fullname


class Quote(models.Model):
    quote = models.CharField(max_length=250)
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.quote
