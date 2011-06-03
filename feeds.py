from django.contrib.syndication.feeds import Feed
from blog.models import Post
from taggit.models import TaggedItem

class LatestBlogFeed(Feed):
    '''Basic feed configuration

    You need to derive your own class from this to set link, and you will
    probably also want to change description and title.

    See http://docs.djangoproject.com/en/1.2/ref/contrib/syndication/
    '''
    description = 'Blog Posts'
    title = 'Blog'
    link ='/blog/'

    def categories(self):
        return TaggedItem.tags_for(Post)

    def items(self):
        return Post.objects.current()

    def item_title(self, item):
        return item.title

    def item_author_name(self, item):
        return item.posted_by.get_full_name()

    def item_pubdate(self, item):
        return item.post_date

    def item_categories(self, item):
        return item.tags.all()


class BlogTagFeed(LatestBlogFeed):
    def get_object(self, request, tags):
        tags = [ tag.strip() for tag in tags.split('/') ]
        return tags

    def description(self, obj):
        return "Posts with tags %s" % (', '.join(obj))
