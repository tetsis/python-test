from django.db import models

# Create your models here.
class Table(models.Model):
    name = models.CharField(max_length=128, default="")

    def __str__(self):
        return self.name
