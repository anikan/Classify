from django.db import models

# Create your models here.

#Class: Has teachers
class SDClass(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    #pub_date = models.DateTimeField('date published')

    def __unicode__(self):
        return self.title + " " + self.description

#Teacher: Has rating and quarters teaching. Specific to class.
class Teacher(models.Model):
    #Name of teacher
    name = models.CharField(max_length=200, default="")

    #Average of cape and RMP overall ratings
    aggregateRating = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    #First rating of teacher for that class on CAPE
    capeRating = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    #RateMyProfessor overall rating
    rateMyProfRating = models.DecimalField(max_digits=4, decimal_places=1, default=0)

    #Average grade for that first class on CAPE
    averageGrade = models.CharField(max_length=10, default="")

    #Response rate for the first class on CAPE,
    responseRate = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    #A class has several teachers.
    specificClass = models.ForeignKey('SDClass')

    #quarterFlags
    quarters = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name + " " + self.rating + " " + self.averageGrade + " " + self.responseRate + " " + self.quarters + " " + self.specificClass