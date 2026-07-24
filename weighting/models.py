from datetime import date

from django.contrib.auth.models import User
from django.db import models


class Weighting(models.Model):
    athlete = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    weight = models.IntegerField('Weight')
    date = models.DateField('Date', default=date.today)

    def __str__(self):
        return f"{self.date}:  {self.weight}kg"
