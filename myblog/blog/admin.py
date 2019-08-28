from django.contrib import admin
from .models import Article
# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'content','time')
    list_filter = ('time',)

admin.site.register(Article,ArticleAdmin)
# admin.register(Article)
