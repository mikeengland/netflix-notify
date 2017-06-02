class TitleTypes:
    """
    The type of the title e.g. if it is a TV show, movie or cinematic release 
    """
    SHOW = 'show'
    MOVIE = 'movie'
    CINEMA_RELEASE = 'cinema_release'

    ALL = ((SHOW, 'Show'),
           (MOVIE, 'Movie'),
           (CINEMA_RELEASE, 'Cinema Release'))


class Languages:
    """
    The language of the title
    """
    EN = 'en'

    ALL = ((EN, 'EN'),)


class Regions:
    """
    The Netflix region
    """
    UK = 'uk'

    ALL = ((UK, 'UK'),)
