from django.db import models
from django.contrib.auth.models import User

class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Test(models.Model):
    text1 = models.TextField()
    text2 = models.TextField()
    text3 = models.TextField()
    description = models.TextField()

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

class Sitting(models.Model):
    user = models.ForeignKey(User)
    test = models.ForeignKey(Test)
    is_active = models.BooleanField(default=False)

class Answer(models.Model):
    sitting = models.ForeignKey(Sitting)
    test = models.ForeignKey(Test)
    question = models.ForeignKey(Question)
    answer_idx = models.IntegerField(default=0)

class Activation(models.Model):
    user = models.ForeignKey(User)
    expiry = DateField()

class Scaling(models.Model)
    min_score = models.IntegerField()
    max_score = models.IntegerField()
    scaled = models.IntegerField()
