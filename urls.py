from django.conf.urls.defaults import patterns, url

#from blog.views import PostList, PostDetail
#
urlpatterns = patterns('',
#    url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[\w-]+)/$',
#        PostDetail.as_view(),
#        name='blog-detail',
#    ),
    url(r'^$', 'blog.views.post_list', name='blog_postlist'),
    url(r'^(?P<category_slug>[\w-]+)/$', 'blog.views.post_list', name='blog_category'),
    url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[\w-]+)/$',
        'blog.views.post_details', name='blog_detail',
    ),
    url(r'^tags/(?P<tag>[\w-]+)/$', 'blog.views.post_tagged', name='blog_post_tagged'),
)
