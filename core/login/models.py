from django.db import models

# Create your models here.
class Visita(models.Model):
    id = models.AutoField(primary_key=True)
    mpId = models.IntegerField()
    policialId = models.IntegerField()
    data = models.DateField()
    horaInicio = models.TimeField()
    horaFim = models.TimeField()
    status = models.CharField(max_length=50)
    presente = models.BooleanField()

    def __str__(self):
        return f"Visita {self.id} - {self.data} {self.horaInicio}"
    