from django.db import models
from datetime import date
from django.contrib.auth.models import User

class DayOfEating(models.Model):
    date = models.DateField('Date', default=date.today)
    kcal = models.IntegerField('Calories', blank=True, null=True)
    protein = models.IntegerField('Protein', blank=True, null=True)
    athlete = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    class Meta:
        verbose_name = 'Day of eating'
        verbose_name_plural = 'Days of eating'
    def __str__(self):
        return f"{self.athlete} {self.date}"
    def __repr__(self):
        return f"{self.date}, {self.kcal} kcal, {self.protein} protein"
    def add_calories(self, kcal):
        self.kcal += int(kcal)
    def add_protein(self, protein):
        self.protein += int(protein)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user.username}"

class Weighting(models.Model):
    athlete = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    weight = models.IntegerField('Weight')
    date = models.DateField('Date', default=date.today)
    def __str__(self):
        return f"{self.date}:  {self.weight}kg"