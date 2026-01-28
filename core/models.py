from django.db import models




class files(models.Model):
    filename = models.CharField(max_length=255)
    file = models.FileField(upload_to="uploads/")
    characters = models.IntegerField()

class contactforms(models.Model):
    email = models.CharField(max_length=255)
    formcontent = models.CharField()
    date_of_form = models.DateField(auto_now=True)