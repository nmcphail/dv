from django.db import models

class CodegenParameters(models.Model):
    
    name  = models.CharField(max_length=200)
    value_string = models.CharField(max_length=200, blank=True)
    value_int = models.IntegerField(default = 0, blank=True)

    def __str__(self):
        return self.name
# Create your models here.
