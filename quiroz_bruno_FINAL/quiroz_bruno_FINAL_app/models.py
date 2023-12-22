from django.db import models

class Institucion(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Inscrito(models.Model):
    ESTADOS = [
        ('RESERVADO', 'Reservado'),
        ('COMPLETADA', 'Completada'),
        ('ANULADA', 'Anulada'),
        ('NO_ASISTEN', 'No Asisten'),
    ]

    id_persona = models.AutoField(primary_key=True)
    nombre_persona = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    fecha_inscripcion = models.DateField(auto_now_add=True)
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE)
    hora_inscripcion = models.TimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS)
    observacion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre_persona

    class Meta:
        db_table = 'django_seminario'