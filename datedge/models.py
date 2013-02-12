from django.db import models
from django.contrib.auth.models import User

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
    is_active = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

class Answer(models.Model):
    sitting = models.ForeignKey(Sitting)
    question = models.ManyToManyField(Question)
    answer_idx = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

class Activation(models.Model):
    user = models.ForeignKey(User)
    expiry = models.DateField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

class Scaling(models.Model):
    min_score = models.IntegerField()
    max_score = models.IntegerField()
    scaled = models.IntegerField()

class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

