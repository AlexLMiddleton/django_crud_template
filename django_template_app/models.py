from django.db import models

class NewModel(models.Model):
    id = models.AutoField(primary_key=True)
    location_code = models.CharField(max_length=3)
