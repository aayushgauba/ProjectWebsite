from django.db import models

class Project(models.Model):
    Title = models.CharField(max_length=100)
    Description = models.TextField()

class Table(models.Model):
    Title = models.CharField(max_length=100)
    Fields = models.IntegerField()
    Project_id = models.IntegerField()

class Fields(models.Model):
    Field = models.CharField(max_length=100)
    Type = models.CharField(max_length=20)
    Table_id = models.IntegerField()
    Order = models.IntegerField()

class Data(models.Model):
    Data = models.CharField(max_length=300)
    Field_id = models.IntegerField()
    Table_id = models.IntegerField()
    Order = models.IntegerField()