from django.contrib import admin 
from celestial.models import *

class PostModelAdmin(admin.ModelAdmin):
    list_display: list = ['shown_name','prompt', 'updated', 'created_on', 'published_on', 'draft']
    list_display_links: list = ['shown_name']
    list_filter: list = ['updated', 'created_on', 'published_on']
    list_editable: list = ['draft']
    search_fields: list = ['shown_name', 'prompt']
    list_per_page: int = 10
    ordering: tuple = ('-id',)

class Meta:
    model: Post = Post

# class TopicModelAdmin(admin.ModelAdmin):
#     list_display: list = ['title', 'description', 'created_on', 'starts_on', 'finished_on', 'active']
#     list_display_links: list = ['title']
#     list_filter: list = ['created_on', 'starts_on', 'finished_on', 'active']
#     search_fields: list = ['title', 'description']
#     list_per_page: int = 10
#     ordering: tuple = ('-starts_on', 'title')

#     class Meta:
#         model: Topic = Topic
        
# class UserProfileModelAdmin(admin.ModelAdmin):
#     list_display: list = ['shown_name', 'device_id', 'magic']
#     list_display_links: list = ['shown_name']
#     list_filter: list = ['magic']
#     search_fields: list = ['shown_name']
#     list_per_page: int = 10
#     ordering: tuple = ('shown_name',)

#     class Meta:
#         model: UserProfile = UserProfile


class configsModelAdmin(admin.ModelAdmin):
    list_display: list = ['id','key','value']
    list_display_links: list = ['id']
    list_filter: list = ['key', 'value']
    list_editable: list = ['key', 'value']
    search_fields: list = ['key', 'value']
    list_per_page: int = 10
    ordering: tuple = ('-id',)

class Meta:
    model: configs = configs

admin.site.register([Post], PostModelAdmin)
# admin.site.register([Topic], TopicModelAdmin)
# admin.site.register([UserProfile], UserProfileModelAdmin)
admin.site.register([configs], configsModelAdmin)