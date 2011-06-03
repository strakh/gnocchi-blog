from django.contrib import admin
from blog import models, forms

register = admin.site.register

class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'published',
        'post_date',
        'kill_date',
        'posted_by',
        'allow_comments',
    )
    list_filter = ('posted_by', 'published',)
    date_heirarchy = 'post_date'
    search_fields = ('title', 'content',)
    prepopulated_fields = {'slug': ('title',)}
    exclude = ('posted_by',)

    form = forms.PostAdminForm
    fieldsets = (
        (None, {
            'fields': ('title', 'slug',),
        },),
        ('Content', {
            'classes': ('wide',),
            'fields': ('content',),
        },),
        ('Extras', {
            'fields': (
                ('published', 'post_date', 'kill_date',),
                ('auto', 'tags', 'allow_comments'),
            ),
        },),
    )

    def queryset(self, request):
        qset = self.model.objects.all()
        if not request.user.is_superuser:
            return qset.filter(posted_by=request.user)
        return qset

    def save_model(self, request, obj, form, change):
        if not change:
            # initial posting
            obj.posted_by = request.user
        obj.save()

register(models.Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post_date', 'post', 'name', 'email', 'ip_address',
        'is_public', 'is_removed',)
    list_filter = ('is_public', 'is_removed', 'user_name',)
    date_heirarchy = ('post_date',)
    search_fieklds = ('user_name', 'comment',)

register(models.Comment, CommentAdmin)
