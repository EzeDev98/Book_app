from django.db import models

# Create your models here.
class Story(models.Model):
    book_title = models.CharField(max_length=250)
    story_title = models.CharField(max_length=250, default='Malik')
    chapter = models.CharField(max_length=250, default='Chapter 1')
    edition = models.CharField(max_length=250)
    origin = models.CharField(max_length=250)
    language = models.CharField(max_length=250)
    author = models.CharField(max_length=250)
    story_body = models.TextField()
    created_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.book_title