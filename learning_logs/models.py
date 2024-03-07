from django.db import models


class Topic(models.Model):
    """Topic learned by the user"""

    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return model representation in form of string"""
        return self.text


class Entry(models.Model):
    """Concrete info o learning progress"""

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "entries"

    def __str__(self):
        """Return model representation in form of string"""
        return f"{self.text[:50]}..."
