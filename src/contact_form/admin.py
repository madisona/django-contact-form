
from django.contrib import admin

from contact_form import models

class ContactEmailAdmin(admin.ModelAdmin):
    model = models.ContactEmail
    search_fields = ("name", "email", "message")
    list_display = ("name", "email", "creationtime")

admin.site.register(models.ContactEmail, ContactEmailAdmin)