from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Question(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title[:50]

class Answer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    content = models.TextField()
    likes = models.ManyToManyField(User,related_name="liked_answers",blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:50]