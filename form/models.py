from django.db import models

# Create your models here.

#Model that will store the top 10 words found from the url
class WordFrequency(models.Model):
    url = models.URLField(max_length = 200)
    word = models.CharField(max_length = 120)
    freq = models.IntegerField()

    # def __str__(self):
    #     return self.word
