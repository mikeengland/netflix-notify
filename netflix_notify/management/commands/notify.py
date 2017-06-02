import logging
from datetime import (datetime,
                      timedelta)

from django.core.management.base import BaseCommand

from netflix_notify.models import (Title,
                                   Notification,
                                   Watcher)

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        titles = Title.objects.filter(active=True).values_list('name')
        titles = {name.lower() for name in titles}

        watchers = Watcher.objects.filter(verified=True, active=True).prefetch_related('notification_set')

        for watcher in watchers:

            # move on if the title is still not present in the Netflix catalogue
            if watcher.title.lower() not in titles:
                continue

            # move on if the last notification for this title was within 90 days
            ninety_days_ago = datetime.now() - timedelta(days=90)
            last_notification_time = watcher.notification_set.order_by('time').last().notification_time

            if last_notification_time > ninety_days_ago:
                continue

            # TODO send an email notification


