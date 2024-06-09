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

class Muscle(models.Model):
    name = models.CharField('Name', max_length=30)
    body_part = models.CharField('Body part', null=True, blank=True, max_length=30)

class Equipment(models.Model):
    name = models.CharField('Name', max_length=30)
    type = models.CharField('Equipment type', null=True, blank=True, max_length=50)

class WorkoutType(models.Model):
    name = models.CharField('Name', max_length=20)
    description = models.CharField('Workout type', null=True, blank=True, max_length=300)

class Exercise(models.Model):
    name = models.CharField('Name', max_length=50)
    description = models.CharField('Workout type', null=True, blank=True, max_length=300)
    muscle = models.ForeignKey(Muscle, on_delete=models.SET_NULL, null=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.SET_NULL, null=True)

class Workout(models.Model):
    date = models.DateField('Date', default=date.today)
    athlete = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    type = models.ForeignKey(WorkoutType, on_delete=models.SET_NULL, null=True, blank=True)

class Set(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    weight = models.CharField('Weight', max_length=15)
    reps = models.IntegerField('Reps')
