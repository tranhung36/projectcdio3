from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
<<<<<<< HEAD
    published = models.BooleanField(default=True)
=======
>>>>>>> d9126545366a992dec1d26c71856227db91d90d6
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE) # models.CASCADE just delete author not delete User

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    

<<<<<<< HEAD
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=True)

    def __str__(self):
        return '{} by {}'.format(self.post.title, str(self.user.username))
    
=======
>>>>>>> d9126545366a992dec1d26c71856227db91d90d6

    
