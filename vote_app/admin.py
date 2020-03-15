from django.contrib import admin
from vote_app.models import Activity, ActivityDetail, VoteRecord
# Register your models here.


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['title', 'img', 'content', 'rule',
                    'start_time', 'end_time', 'active']
    search_fields = ['title']


@admin.register(ActivityDetail)
class ActivityDetailAdmin(admin.ModelAdmin):
    list_display = ['activity_id', 'name', 'vote_count', 'thumb', 'file']
    search_fields = ['name']
    # readonly_fields = ['vote_count']


@admin.register(VoteRecord)
class VoteRecordAdmin(admin.ModelAdmin):
    list_display = ['activity_detail_id', 'activity_type', 'IP', 'vote_time']
    search_fields = ['activity_detail_id']
    readonly_fields = ['vote_time']
