from django.db import models

# Create your models here.

#Class: Has teachers
class SDClass(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    #pub_date = models.DateTimeField('date published')

    def __unicode__(self):
        return self.title

#Teacher: Has rating and quarters teaching. Specific to class.
class Teacher(models.Model):
    #Name of teacher
    name = models.CharField(max_length=200)

    #First rating of teacher for that class on CAPE
    rating = models.DecimalField(max_digits=3, decimal_places=2)

    #A class has several teachers.
    specificClass = models.ForeignKey('SDClass')

    #quarterFlags
    quarters = models.IntegerField()