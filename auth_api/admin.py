from django.contrib import admin
from .models import User_profile , follow , email_validator
# Register your models here.

admin.site.register(User_profile)
admin.site.register(follow)
admin.site.register(email_validator)