class Settings(object):
    SECRET_KEY = 'CHANGEME'
    FLATPAGES_EXTENSION = '.md'
    FLATPAGES_MARKDOWN_EXTENSIONS = ['codehilite', 'headerid', 'smartypants']
    FREEZER_IGNORE_MIMETYPE_WARNINGS=True
    FREEZER_REMOVE_EXTRA_FILES=True
    DEBUG = True
    FREEZER_BASE_URL='http://www.example.com/'
    BLAG_TITLE='Untitled Blog'
    BLAG_DESCRIPTION='Undescribed Blog'
    BLAG_AUTHOR='Unknown Soldier'
