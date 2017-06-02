import logging

import requests
from .enums import TitleTypes
logger = logging.getLogger(__name__)


class ScraperError(Exception):
    pass


class Scraper:
    """
    Scrapes the JustWatch API for Netflix Titles
    """
    BASE_URL = 'https://apis.justwatch.com/content/titles/en_GB/popular'

    QUERY_PARAMS = ('?body=%7B%22{title_type}%22:null,%22content_types%22:null,%22genres%22:null,'
                    '%22languages%22:null,%22max_price%22:null,%22min_price%22:null,'
                    '%22monetization_types%22:%5B%22flatrate%22,%22rent%22,%22buy%22,%22free%22,%22ads%22%5D,'
                    '%22page%22:{page_number},%22page_size%22:200,%22presentation_types%22:null,'
                    '%22providers%22:%5B%22nfx%22%5D,%22release_year_from%22:null,'
                    '%22release_year_until%22:null,%22scoring_filter_types%22:null%7D')

    URL = BASE_URL + QUERY_PARAMS

    def __init__(self):
        self.titles = []

    def get_titles(self):
        """
        Gets titles from an API for TV shows, movies and cinematic releases, deduplicates them
        and returns them as a list.
        
        :return: List of dicts (title information)
        """
        del self.titles[:]  # we don't want to keep expanding the list if the method is run multiple times

        # Get all titles for cinematic releases, movies and shows
        for title_type in TitleTypes.ALL:
            self._get_titles(page_number=1, title_type=title_type)

        # Dedupe the list in case of any overlaps from the different title endpoints
        # First, remove the mutable scoring key so we can dedupe it easily using the method below.
        titles_to_dedupe = set()
        for title in self.titles:
            del title['scoring']
            titles_to_dedupe.add(tuple(sorted(title.items())))

        return [dict(title) for title in titles_to_dedupe]

    def _get_titles(self, page_number, title_type):
        """
        Recursively get titles. We do this as the API endpoint is paginated so we get a single
        page of data at a time.
        
        :param page_number: The page number for the API pagination
        :param title_type: The type of title get titles for e.g. show or movie
        :return: 
        """
        url = self.URL.format(page_number=page_number, title_type=title_type)
        response = requests.get(url)

        if not response.status_code == 200:
            raise ScraperError('Error returned from the JustWatch API. Status code is {}.'.format(response.status_code))

        response_data = response.json()

        self.titles += response_data['items']

        if page_number < response_data['total_pages']:
            self._get_titles(page_number + 1, title_type)
