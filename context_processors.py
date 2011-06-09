from django.conf import settings
from blog.models import Category

def categories_to_nav(request):
    def get_categories():
      return Category.objects.all()

    return {
        'categories': get_categories(),
    }

