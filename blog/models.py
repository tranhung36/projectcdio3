from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image



class Country(models.Model):
    country_name = models.CharField(max_length=50)

    def __str__(self):
        return self.country_name


class Place(models.Model):
    place_name = models.CharField(max_length=50)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.place_name
        

class Post(models.Model):
    title = models.CharField('Tiêu đề' ,max_length=100)
    content = models.TextField('Nội dung')
    published = models.BooleanField(default=True)
    date_posted = models.DateTimeField(default=timezone.now)
    liked = models.ManyToManyField(User, default=None, blank=True, related_name='liked')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, default='')
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_pics', verbose_name='image')


    def __str__(self):
        return self.title
    

    @property
    def num_likes(self):
        return self.liked.all().count()


    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 800 or img.width > 600:
            output_size = (800, 600)
            img.thumbnail(output_size)
            img.save(self.image.path)

   

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    content = models.TextField('Nội dung', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=True)
    parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE, related_name='replies')

    def __str__(self):
        return '{} by {}'.format(self.post.title, str(self.user.username))
    
    
