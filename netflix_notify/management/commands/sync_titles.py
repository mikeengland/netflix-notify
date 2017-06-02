import logging

from django.core.management.base import BaseCommand

from netflix_notify.enums import Regions
from netflix_notify.models import (Title,
                                   SyncLog)
from netflix_notify.scraper import Scraper

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Sync the titles with the application database'

    def add_arguments(self, parser):
        # TODO Add option to sync a specific Netflix region
        pass

    def handle(self, *args, **options):
        self.get_and_store_titles()

    def get_and_store_titles(self):
        """
        Retrieve the titles from the API, post-process them and store them in the database, ensuring
        any existing but now missing titles are set as inactive.
        """
        logger.info('Retrieving titles from the API')
        scraper = Scraper()
        titles = scraper.get_titles()

        created_or_updated = []

        logger.info('Syncing titles in the database')

        for title in titles:
            title, _ = Title.objects.update_or_create(title_type=title.get('object_type'),
                                                      name=title.get('title'),
                                                      description=title.get('short_description'),
                                                      language=title.get('original_language'),
                                                      release_year=title.get('original_release_year'),
                                                      runtime=title.get('runtime'),
                                                      netflix_region=Regions.UK,
                                                      active=True)
            created_or_updated.append(title)

        currently_active = [title.pk for title in created_or_updated]
        Title.objects.exclude(pk__in=currently_active).update(active=False)

        SyncLog.objects.create()
        logger.info('Title sync complete!')
