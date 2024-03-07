from django.db import models


class Topic(models.Model):
    """Topic learned by the user"""

    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return model representation in form of string"""
        return self.text
