from django.contrib import admin

from .models import *

admin.site.register(MyUser)
admin.site.register(UserProfile)
admin.site.register(CompanyProfile)