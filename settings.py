from django.conf import settings

BLOG_USERNAME_URLS = getattr(settings, 'BLOG_USERNAME_URLS', False)
BLOG_DATEBASED_URLS = getattr(settings, 'BLOG_DATEBASED_URLS', True)
