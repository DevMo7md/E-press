from django.contrib import admin
from .models import *
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin


class ArticleAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)  # الحقول التي ستستخدم Summernote
    readonly_fields = ('add_date', 'edit_date')

admin.site.register(Article, ArticleAdmin)


# Register your models here.
admin.site.register(Journalist)
admin.site.register(Category)
admin.site.register(Advertisment)
admin.site.register(Comment)
admin.site.register(Contact)
