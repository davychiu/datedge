from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime
import time

class Test(models.Model):
    text1 = models.TextField()
    text2 = models.TextField()
    text3 = models.TextField()
    
    def __unicode__(self):
        return self.text1[:50]

class Question(models.Model):
    test = models.ForeignKey(Test)
    text_idx = models.IntegerField(default=0)
    option1 = models.CharField(max_length=500)
    option2 = models.CharField(max_length=500)
    option3 = models.CharField(max_length=500)
    option4 = models.CharField(max_length=500)
    option5 = models.CharField(max_length=500)
    answer_idx = models.IntegerField(default=0)
    description = models.TextField()

    def __unicode__(self):
        return self.description

class Sitting(models.Model):
    user = models.ForeignKey(User)
    test = models.ForeignKey(Test)
    is_timed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_date',)

    def __unicode__(self):
        return u't: %s a: %s c: %s m: %s' % (self.test_id, self.is_active, self.created_date, self.modified_date)

    def _score(self):
        score = 0
        for q in self.test.question_set.filter(answer__sitting=self):
            if q.answer_idx == self.test.question_set.get(id=q.id).answer_set.get(sitting=self,question=q).answer_idx:
                score += 1
        return score

    def _score_scaled(self):
        score = self.score
        try:
            scaled = Scaling.objects.get(max_score__gte=score, min_score__lte=score).scaled
        except Scaling.DoesNotExist:
            scaled = 0
        return scaled

    def _score_percent(self):
        return "%.0f%%" % (float(self.score) / 50 * 100)

    def _marked(self):
        return self.test.question_set.filter(answer__is_marked=True, answer__sitting=self)
    
    def _complete(self):
        return self.test.question_set.filter(answer__answer_idx__isnull=False, answer__sitting=self)

    def _timerstring(self):
        t = self.created_date
        offset = time.timezone if (time.localtime().tm_isdst == 0) else time.altzone
        offset = offset / 60 / 60 * -1
        return u'%i, %i, %i, %i, %i, %i, %i' % (0, t.year, t.month-1, t.day, t.hour+1, t.minute, t.second)

    score = property(_score)
    score_scaled = property(_score_scaled)
    score_percent = property(_score_percent)
    marked = property(_marked)
    complete = property(_complete)
    timerstring = property(_timerstring)

class Answer(models.Model):
    sitting = models.ForeignKey(Sitting)
    question = models.ForeignKey(Question)
    user = models.ForeignKey(User)
    answer_idx = models.IntegerField(null=True, blank=True)
    is_marked = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u's: %s q: %s u: %s a: %s'%(self.sitting.id, self.question.id, self.user.id, self.answer_idx)

class Activation(models.Model):
    user = models.ForeignKey(User)
    expiry = models.DateField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.user.username

    def _is_active(self):
        today = date.today()
        if self.objects.filter(user=self.user, expiry__gte=today):
            return True
        else:
            return False

class Scaling(models.Model):
    min_score = models.IntegerField()
    max_score = models.IntegerField()
    scaled = models.IntegerField()

class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

