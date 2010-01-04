from django.contrib import admin
from jaxerprofile.models import UserProfile

class AdminUserProfile(admin.ModelAdmin):
    list_display = ('username','name','os','language')

admin.site.register(UserProfile, AdminUserProfile)