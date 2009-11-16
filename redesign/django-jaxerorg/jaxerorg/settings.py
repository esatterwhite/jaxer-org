#########################################################################
#                     READ ME FIRST
#
#        This settings file is an example set up.
#        you should let Django create a unique project
#        and copy and past the bits from this file that you need:
#        development_mode, installed_app, profile_module, middlewares, 
#        sorl settings, etc
#
#########################################################################


DEVLOPMENT_MODE = True
MAINTENANCE_MODE = False

if DEVLOPMENT_MODE:
    DEBUG = True
    TEMPLATE_DEBUG = True
    TEMPLATE_STRING_IF_INVALID = 'INVALID VARIABLE'
    #CACHE_BACKEND = 'locmem:///'
    SESSION_EXPIRE_AT_BROWSER_CLOSE = False
else:
    DEBUG = False
    TEMPLATE_DEBUG = False
    TEMPLATE_STRING_IF_INVALID = ''
    SESSION_EXPIRE_AT_BROWSER_CLOSE = True
  
ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = ''           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'jaxerorg'             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.


TIME_ZONE = 'America/Chicago'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1
INTERNAL_IPS = ('127.0.0.1',)

USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = 'jaxermedia/'
STATIC_DOC_ROOT = ''
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'http://127.0.0.1:8000/static_media/'

ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
    'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

MIDDLEWARE_CLASSES = (
#    'django.middleware.cache.UpdateCacheMiddleware', #uncomment to use caching
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'maintenancemode.middleware.MaintenanceModeMiddleware',
#   'debug_toolbar.middleware.DebugToolbarMiddleware',       #uncomment to use debug toolbar
#    'django.middleware.cache.FetchFromCacheMiddleware',  # uncomment to use caching
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug', # comment out when in production
    'django.core.context_processors.media',
    'django.core.context_processors.request',
)
THUMBNAIL_PROCESSORS = (
    # Default processors - sorl thumbnail
    'sorl.thumbnail.processors.colorspace',
    'sorl.thumbnail.processors.autocrop',
    'sorl.thumbnail.processors.scale_and_crop',
    'sorl.thumbnail.processors.filters',
    )
APPEND_SLASH = True
ROOT_URLCONF = 'jaxerorg.urls'
AUTH_PROFILE_MODULE ='jaxerprofile.userprofile'
INSTALLED_APPS = (
    'django_extensions',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.comments',
    'django.contrib.sites',
    'django.contrib.humanize',
    'jaxerorg.core',
    'jaxerlog',
    'jaxerblog',
    'jaxerorg.jaxerprofile',
    'pagination',
    'sorl.thumbnail',
    'hotsauce',
    'pagination',
    'template_utils',
    'registration',
    'tagging',
    'messages',
    'grappelli',
    'notification',    
)
