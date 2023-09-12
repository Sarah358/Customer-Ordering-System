from django.contrib import admin

from .models import Profile


# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "pkid", "user", "phone_number", "city", "address"]
    list_filter = ["phone_number", "address", "city"]
    list_display_links = ["id", "user"]


admin.site.register(Profile, ProfileAdmin)
