from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Pageant(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    is_closed = models.BooleanField(default=False, null=False)

    def __unicode__(self):
        return self.title

class CriteriaCategory(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    pageant = models.ForeignKey(Pageant)
    weight = models.FloatField(null=False)

    def __unicode__(self):
        return self.name

class Criteria(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    weight = models.FloatField(null=False)
    maximum_score = models.FloatField(null=False)
    category = models.ForeignKey(CriteriaCategory)

    def __unicode__(self):
        return self.name


class ParticipantGroup(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    pageant  = models.ForeignKey(Pageant)

    def __unicode__(self):
        return self.name

class PageantParticipant(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    order = models.IntegerField(null=True, blank=True)
    deduction = models.FloatField(null=False, default=0)    
    group = models.ForeignKey(ParticipantGroup)
    photo = models.FileField(upload_to="profile/", null=True, blank=True)

    def __unicode__(self):
        return self.name

class Judge(models.Model):
    user = models.ForeignKey(User, related_name="+")
    pageant = models.ForeignKey(Pageant)

    def __unicode__(self):
        return '%s' % self.user

class PageantParticipantRating (models.Model):
    participant = models.ForeignKey(PageantParticipant)
    criteria = models.ForeignKey(Criteria)
    judge = models.ForeignKey(Judge)
    rating = models.FloatField(null=True)