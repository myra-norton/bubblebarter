from django.contrib import admin

from .models import UserDetails, Item, Proposal, Report
# Register your models here.

admin.site.register(UserDetails)
admin.site.register(Item)
admin.site.register(Proposal)
admin.site.register(Report)
