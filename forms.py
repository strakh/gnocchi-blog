from django import forms
from blog import models
from taggit.models import TaggedItem
import re

class PostAdminForm(forms.ModelForm):
    auto = forms.BooleanField(label='Auto-tag?', required=False,
        help_text="Automatically scan content for tags"
    )
    class Meta:
        model = models.Post
    def clean(self):
        data = self.cleaned_data
        if data['auto']:
            tags = set(data['tags'])
            tags.update([
                tag
                for tag in TaggedItem.tags_for(models.Post)
                if re.search(r'\b%s\b' % tag.name, data['content'], re.I|re.M)
            ])
            data['tags'] = list(tags)
        return data

class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = (
            'user_name',
            'user_email',
            'content',
        )

class SimpleCommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = (
            'content',
        )
