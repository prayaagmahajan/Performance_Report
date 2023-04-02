from django.contrib import admin
from .models import Profile,Document,Student,Subject,Mark
# Register your models here.

admin.site.register(Profile)
admin.site.register(Document)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Mark)