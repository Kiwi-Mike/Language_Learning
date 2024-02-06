from django.db import models

# Create your models here.

class Card(models.Model):
    korean = models.CharField(max_length=100)
    english = models.CharField(max_length=100)

    # Box can also be thought of as a category
    box = models.CharField(max_length=100)

    last_tested = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.korean, self.english