

from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.title

class Rating(models.Model):
    post = models.ForeignKey(Post, related_name='rating', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    class Meta:
        unique_together = ('post', 'user')
        indexes = [
            models.Index(fields=['post', 'user']),
        ]

    def __str__(self):
        return f'{self.user} - {self.post} - {self.score}'







