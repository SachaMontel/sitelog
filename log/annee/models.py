from django.db import models

# Create your models here.

class Message(models.Model):
    texte = models.TextField()
    auteur = models.CharField(max_length=200)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"{self.auteur}: {self.texte[:50]}..."
