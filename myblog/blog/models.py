from __future__ import unicode_literals
from django.db import models
class Article(models.Model):
    id = models.IntegerField(primary_key=True,auto_created=True,serialize=False,verbose_name='ID')
    title = models.CharField(max_length=64,default='Title')
    small_content = models.TextField(null=True)
    content = models.TextField(null=True)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    __repr__ = __str__