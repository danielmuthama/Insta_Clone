from django.db import models
from accounts.models import UserAccount
from cloudinary.models import CloudinaryField

class Post(models.Model):
    host = models.ForeignKey(UserAccount, on_delete=models.SET_NULL, null=True)
    image = CloudinaryField("image")
    description = models.CharField(max_length=100)
    liked = models.ManyToManyField(UserAccount, blank=True, null=True, related_name='liked')
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description


class Comment(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='users')
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name='comments')
    body = models.CharField(max_length=200)
    date_posted = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_posted']
        
    def __str__(self):
        return self.body


LIKED_CHOICES = (
    ('like', 'like'),
    ('unlike', 'unlike')
)
class Like(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKED_CHOICES, max_length=10)

    def __str__(self):
        return str(self.post)

