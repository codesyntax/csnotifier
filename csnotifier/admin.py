from csnotifier.models import Notification
from csnotifier.models import Device
from django.contrib import admin


def mark_as_sent(modeladmin, request, queryset):
    queryset.update(sent=True)
mark_as_sent.short_description = "Mark these notifications as SENT"

def mark_as_not_sent(modeladmin, request, queryset):
    queryset.update(sent=False)
mark_as_not_sent.short_description = "Mark these notifications as NOT SENT"


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'tags', 'data', 'sent')
    actions = [mark_as_sent, mark_as_not_sent]


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'token', 'tags', 'enabled')



admin.site.register(Notification, NotificationAdmin)
admin.site.register(Device, DeviceAdmin)
