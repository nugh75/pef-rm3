from django.db import models

class TutorCoordinatori(models.Model):
    id = models.AutoField(primary_key=True)  # Aggiungi questa riga
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    email = models.EmailField(max_length=150)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    dipartimento = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nome} {self.cognome}"
