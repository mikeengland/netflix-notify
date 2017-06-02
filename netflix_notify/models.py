from django.db import models
from .enums import (TitleTypes,
                    Languages,
                    Regions)


class Title(models.Model):
    """
    Store title data retrieved by the scraper
    """

    title_type = models.CharField(max_length=32, choices=TitleTypes.ALL)

    netflix_region = models.CharField(max_length=32, choices=Regions.ALL)

    name = models.CharField(max_length=255)

    description = models.TextField()

    release_year = models.IntegerField()

    language = models.CharField(null=True, max_length=32, choices=Languages.ALL)

    # Only movies have a runtime
    runtime = models.IntegerField(null=True)

    # If the title is currently available
    active = models.BooleanField()

    updated_time = models.DateTimeField(auto_now=True)


class Watcher(models.Model):
    """
    A model keeping track of email addresses for notifications.
    """
    email = models.EmailField()

    verified = models.BooleanField(default=False)

    title = models.CharField(max_length=128)

    active = models.BooleanField(default=True)


class Notification(models.Model):
    """
    Keeps track of previously sent notifications
    """
    title = models.ForeignKey(Title)

    watcher = models.ForeignKey(Watcher)

    time = models.DateTimeField(auto_now_add=True)


class SyncLog(models.Model):
    """
    Keep track of each time the titles were synced 
    """
    sync_time = models.DateTimeField(auto_now_add=True)
