from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now
from django.urls import reverse
from django.contrib.auth.models import User

import string
import random

from ckeditor.fields import RichTextField

def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    description = RichTextField()
    image = models.ImageField(upload_to='thubmnails')
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ('-published_at',)


    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('post_detail', args=[self.slug])


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(rand_slug() + "-" + self.title)
        super(Post, self).save(*args, **kwargs)



class Comment(models.Model):
    sno = models.AutoField(primary_key=True)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    commented_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.content[0:13] + '... by ' + self.user.username