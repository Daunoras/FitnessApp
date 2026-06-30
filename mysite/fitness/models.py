from django.db import models
from datetime import date
from django.contrib.auth.models import User


class Muscle(models.Model):
    name = models.CharField('Name', max_length=30)
    body_part = models.CharField('Body part', null=True, blank=True, max_length=30)
    def __str__(self):
        return self.name

class Equipment(models.Model):
    name = models.CharField('Name', max_length=30)
    type = models.CharField('Equipment type', null=True, blank=True, max_length=50)
    def __str__(self):
        return self.name

class WorkoutType(models.Model):
    name = models.CharField('Name', max_length=20)
    description = models.CharField('Workout type', null=True, blank=True, max_length=300)
    def __str__(self):
        return self.name


class Exercise(models.Model):
    name = models.CharField('Name', max_length=50)
    description = models.CharField('Description', null=True, blank=True, max_length=300)
    target_muscle = models.ForeignKey(Muscle, on_delete=models.SET_NULL, null=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.name


class Workout(models.Model):
    date = models.DateField('Date', default=date.today)
    athlete = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    type = models.ForeignKey(WorkoutType, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return f"{self.date} - {self.type}"


class Set(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    weight = models.CharField('Weight', max_length=15)
    reps = models.IntegerField('Reps')
    def __str__(self):
        if self.weight == "0":
            return f"{self.exercise}: bodyweight x {self.reps}"
        else:
            return f"{self.exercise}: {self.weight} kg x {self.reps}"
