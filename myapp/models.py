from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from PIL import Image
from django.apps import apps

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    phone = models.IntegerField(null=True,default="0123456789")
    address = models.CharField(max_length=2000,null=True,default="-")
    profile_image = models.ImageField(default='default.jpg',upload_to='profile_pics')
    github = models.CharField(max_length=100,null=True,default="-")
    twitter = models.CharField(max_length=100,null=True,default="-")
    website = models.CharField(max_length=100,null=True,default="-")
    facebook = models.CharField(max_length=100,null=True,default="-")

    def __str__(self):
        return f'{self.user.username} profile'

    def save(self):
        super().save()

        img = Image.open(self.profile_image.path)

        if img.height > 200 or img.width>200:
            output_size = (200,200)
            img.thumbnail(output_size)
            img.save(self.profile_image.path)


class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    document = models.FileField(upload_to='documents')

    def __str__(self):
        return self.title

class Subject(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username

class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()

    class Meta:
        unique_together = ['student', 'subject']

    def __str__(self):
        return f"{self.student.user.username} - {self.subject.name}: {self.marks}"
