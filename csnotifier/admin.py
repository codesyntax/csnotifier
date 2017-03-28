from csnotifier.models import Notification
from csnotifier.models import Device
from django.contrib import admin

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'tags', 'sent', 'data')


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('uuui', 'token', 'tags', 'enabled')
    


admin.site.register(Notification, NotificationAdmin)
admin.site.register(Device, DeviceAdmin)
