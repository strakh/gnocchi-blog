#from django.views.generic.dates import ArchiveIndexView, DateDetailView
from django.views.generic.date_based import archive_index, object_detail
from django.http import HttpResponseRedirect
from django.db.models import Q
from blog import models, forms
from blog.models import Tag

# This will roll for django-1.3
#class PostMixin(object):
#    date_field = 'post_date'
#    slug_field = 'slug'
#    model = models.Post
#    username = None
#
#    def get_queryset(self):
#        qset = models.Post.objects.current()
#        if self.username:
#            qset = qset.filter(posted_by__username=self.username)
#        for tag in self.request.GET.getlist('tags'):
#            qset = qset.filter(tags__name=tag)
#        return qset
#
#class PostList(PostMixin, ArchiveIndexView):
#    template_name = 'blog/post_list.html'
#    allow_empty = True
#
#class PostDetail(PostMixin, DateDetailView):
#    template_name = 'blog/post_detail.html'
#    context_object_name = 'post'
#
#    def _get_remote_ip(self, request):
#        try:
#            return request.META['HTTP_X_FORWARDED_FOR']
#        except KeyError:
#            return request.META['REMOTE_ADDR']
#
#    def post(self, request, *args, **kwargs):
#        self.object = post = self.get_object()
#        form = forms.CommentForm(self._get_remote_ip(self.request), request.POST)
#        if form.is_valid():
#            comment = form.save(commit=False)
#            comment.post = post
#            comment.ip_address = self._get_remote_ip(self.request)
#            if request.user.is_authenticated():
#                comment.user = request.user
#            comment.save()
#            return HttpResponseRedirect(post.get_absolute_url())
#        context = self.get_context_data(object=post)
#        context['comment_form'] = form
#        return self.render_to_response(context)
#
#    def get_context_data(self, **kwargs):
#        context = super(PostDetail, self).get_context_data(**kwargs)
#        context['comment_form'] = forms.CommentForm(self._get_remote_ip(self.request))
#        return context
#
def post_list(request):
    date_field = 'post_date'
    queryset = models.Post.objects.current()
    for tag in request.GET.getlist('tags'):
        queryset = queryset.filter(tags__name=tag)
    tags = Tag.objects.all()
    return archive_index(request, queryset, date_field, extra_context=dict(page='blog', tags=tags))

def post_details(request, year, month, day, slug):
    if request.user.is_authenticated():
        commentformclass = forms.SimpleCommentForm
    else:
        commentformclass = forms.CommentForm
    def _get_remote_ip(request):
        try:
            return request.META['HTTP_X_FORWARDED_FOR']
        except KeyError:
            return request.META['REMOTE_ADDR']
    date_field = 'post_date'
    queryset = models.Post.objects.filter(slug=slug)
    tags = Tag.objects.all()
    comment_form = commentformclass()
    if request.method == 'POST':
        comment_form = commentformclass(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = models.Post.objects.get(slug=slug)
            comment.ip_address = _get_remote_ip(request)
            if request.user.is_authenticated():
                comment.user = request.user
            comment.save()
            comment_form = commentformclass()
    
    return object_detail(request, queryset=queryset, year=year, month=month, day=day, slug=slug, date_field=date_field, template_object_name='post', extra_context=dict(page='blog', tags=tags, comment_form=comment_form))

def post_tagged(request, tag):
    date_field = 'post_date'
    queryset = models.Post.objects.current().filter(tags__name=tag)
    tags = Tag.objects.all()
    return archive_index(request, queryset, date_field, extra_context=dict(page='blog', tags=tags))
