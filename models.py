from django.db import models
from django.template.defaultfilters import slugify

from blog import settings
from taggit.managers import TaggableManager
from taggit.models import Tag as TaggitTag

from datetime import datetime

class Tag(TaggitTag):
    class Meta:
        proxy=True
        
    @models.permalink
    def get_absolute_url(self):
        return 'blog_post_tagged', (), dict(tag=self.name)

class Category(models.Model):
    title = models.CharField('title', max_length=200)
    slug = models.SlugField('slug', unique=True)
    
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return 'blog_category', (), dict(category_slug=self.slug)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)


class BlogManager(models.Manager):
    def current(self):
        now = datetime.now()
        return self.get_query_set().filter(
            published=True,
            post_date__lte=now,
        ).exclude(
            kill_date__lte=now
        )

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    content = models.TextField(blank=True)
    category = models.ForeignKey(Category, verbose_name='category', related_name='posts')

    post_date = models.DateTimeField(default=datetime.now)
    kill_date = models.DateTimeField(null=True, blank=True, default=None)
    posted_by = models.ForeignKey('auth.User', blank=True, null=True,
        related_name='blog_posts')
    published = models.BooleanField(default=False)

    allow_comments = models.BooleanField(default=False)

    tags = TaggableManager(blank=True)

    objects = BlogManager()

    class Meta:
        ordering = ('-post_date',)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        kwargs = {'slug': self.slug,}
        if settings.BLOG_DATEBASED_URLS:
            kwargs.update({
                'year': '%04d' % self.post_date.year,
                'month': self.post_date.strftime('%b').lower(),
                'day': '%02d' % self.post_date.day,
            })
        if settings.BLOG_USERNAME_URLS:
            kwargs['username'] = self.posted_by.username
        return 'blog_detail', (), kwargs
      
    def public_comments(self):
        return self.comments.filter(is_public=True, is_removed=False)

    def comments_amount(self):
        return self.public_comments().count()
        

class Comment(models.Model):
    '''Mostly a copy of django.contrib.comments Comment model'''
    post = models.ForeignKey(Post, related_name='comments')
    content = models.TextField()

    post_date = models.DateTimeField(default=datetime.now)
    ip_address = models.IPAddressField(blank=True, null=True)

    user = models.ForeignKey('auth.User', null=True, blank=True, related_name='gnoblog_comments')
    user_name = models.CharField(max_length=50)
    user_email  = models.EmailField(blank=True)

    is_public = models.BooleanField(default=True)
    is_removed = models.BooleanField(default=False)

    class Meta:
        ordering = ('post_date',)
    def __unicode__(self):
        return u'%s...' % self.content[:50]

    # Properties for variable values

    def get_name(self):
        if self.user_id:
            return self.user.get_full_name() or self.user.username
        return self.user_name
    def set_name(self, value):
        if self.user_id:
            raise AttributeError("This comment was posted by an authenticated "\
                "user and thus the name is read-only.")
        self.user_name = value
    name = property(get_name, set_name)

    def get_email(self):
        if self.user_id:
            return self.user.email
        return self.user_email
    def set_email(self, value):
        if self.user_id:
            raise AttributeError("This comment was posted by an authenticated "\
                "user and thus the email is read-only.")
        self.user_email = value
    email = property(get_email, set_email)


import akismet
from django.conf import settings
from django.contrib.sites.models import Site 
from django.db.models.signals import pre_save

# Signals
def pre_save_comment(sender, **kargs):
    if 'instance' in kargs:
        comment = kargs['instance']
        print comment
        
        # If in debug mode skip this check with Akismet
        if not settings.DEBUG:
            try:
                real_key = akismet.verify_key(settings.AKISMET_KEY ,Site.objects.get_current().domain)
                if real_key:
                    is_spam = akismet.comment_check(settings.AKISMET_KEY ,Site.objects.get_current().domain, comment.ip_address, None, comment_content=comment.content)
                    if is_spam:
                        comment.is_public = False
                        print "That was spam"
            except akismet.AkismetError, e:
                print e.response, e.statuscode

# disabled temporarily        
#pre_save.connect(pre_save_comment, Comment)
