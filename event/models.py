from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
	title = models.CharField(max_length=255, null=False, blank=False)
	is_closed = models.BooleanField(default=False, null=False)

class Criteria(models.Model):
	event = models.ForeignKey(Event)
	title = models.CharField(max_length=255, null=False, blank=False)
	weight = models.FloatField(null=False)
	maximum_score = models.FloatField(null=False)

class Judge(models.Model):
	user = models.ForeignKey(User)
	event = models.ForeignKey(Event)

class Participant(models.Model):
	name = models.CharField(max_length=255, null=False, blank=False)
	event = models.ForeignKey(Event)
	order = models.IntegerField(null=True, blank=True)
	deduction = models.FloatField(null=False, default=0)

class ParticipantRating(models.Model):
	participant = models.ForeignKey(Participant)
	criteria = models.ForeignKey(Criteria)
	judge = models.ForeignKey(Judge)
	rating = models.FloatField(null=True)