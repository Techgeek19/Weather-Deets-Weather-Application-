from django.db import models

# Create your models here.

class City(models.Model):
    name = models.CharField(max_length=40)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'cities'

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    message = models.TextField()

    def __str__(self):
        return self.name