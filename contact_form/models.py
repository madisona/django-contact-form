
from django.db import models

class ContactEmail(models.Model):
    """
    ContactData model to store contact information in database
    """
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=11, blank=True)
    message = models.TextField()
    creation_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name