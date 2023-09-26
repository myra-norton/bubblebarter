from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User as auth_User

# Create your models here.

class UserDetails(models.Model):
    user = models.OneToOneField(auth_User, on_delete=models.CASCADE, default = 1)
    #netid = models.TextField(max_length=100, primary_key=True)
    #bannedUntil = models.DateTimeField(default=timezone.now)
    itemsstarred = models.JSONField(blank=True, default =list)
    userbio = models.TextField()
    phonenumber = models.IntegerField(blank=True, null=True)


    def __str__(self):
        return f'{self.user}'

class Item(models.Model):
    itemid = models.UUIDField(primary_key=True)
    dateexpires = models.DateTimeField(default=timezone.now() + timezone.timedelta(days=30))
    dateposted = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    isactive = models.BooleanField(default=True)
    isprivate = models.BooleanField(default=False)
    owner = models.TextField(max_length=100)
    title = models.TextField(max_length=100)
    wants = models.TextField()
    value = models.IntegerField(blank=True, null=True)
    image_public_id = models.CharField(max_length=50, blank=True, null=True)
    image_url = models.CharField(max_length=255, null = True)

    # tags
    fun_tag = models.BooleanField(default=False)
    weird_tag = models.BooleanField(default=False)
    event_tag = models.BooleanField(default=False)
    ticket_tag = models.BooleanField(default=False)
    misc_tag = models.BooleanField(default=False)
    free_tag = models.BooleanField(default=False)
    room_tag = models.BooleanField(default=False)
    help_tag = models.BooleanField(default=False)
    art_tag = models.BooleanField(default=False)
    food_tag = models.BooleanField(default=False)
    clothing_tag = models.BooleanField(default=False)
    transport_tag = models.BooleanField(default=False)

    def get_active_tags(self):
        tags = [
            ('Fun', self.fun_tag),
            ('Weird', self.weird_tag),
            ('Event', self.event_tag),
            ('Ticket', self.ticket_tag),
            ('Misc', self.misc_tag),
            ('Free', self.free_tag),
            ('Room', self.room_tag),
            ('Help', self.help_tag),
            ('Art', self.art_tag),
            ('Food', self.food_tag),
            ('Clothing', self.clothing_tag),
            ('Transport', self.transport_tag),
        ]

        return [tag_name for tag_name, is_active in tags if is_active]

    def __str__(self):
        return f'{self.title} : {self.itemid}'

class Proposal(models.Model):
    proposalid = models.UUIDField(primary_key=True)
    dateoffered = models.DateTimeField(auto_now_add=True)
    itembid = models.UUIDField() #item being bid on
    proposaltext = models.TextField(blank=True, null=True)
    proposedto = models.TextField(max_length=100)
    proposer = models.TextField(max_length=100)
    status = models.TextField(max_length=100)
    itemid = models.UUIDField()
    dateupdated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.proposer} -> {self.proposedto} : {self.proposalid}'

class Report(models.Model):
    reportid = models.UUIDField(primary_key=True)
    actiontaken = models.TextField(default=None, null=True)
    reportdate = models.DateTimeField(auto_now_add=True)
    reporteduser = models.TextField(max_length=100)
    reporter = models.TextField(max_length=100)
    reporteditemid = models.TextField(default=None, null=True, blank=True)
    reportedproposalid = models.TextField(default=None, null=True, blank=True)
    reportstatus = models.TextField(max_length=100, default="pending")
    reporttext = models.TextField()

    def __str__(self):
        return f'{self.reporter} reports {self.reporteduser} : {self.reportid}'
