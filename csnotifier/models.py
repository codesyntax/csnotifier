import uuid
from django.db import models
from .notifications import send_request

class DeviceManager(models.Manager):
    def register_device(self,token):
        device_id = uuid.uuid4().get_hex().replace('-','')
        device = Device.objects.create(uuid=device_id,
                                       token=token)
        return device
    
    def enabled(self):
        return super(DeviceManager, self).get_queryset().filter(enabled=True)
    
    def search(self, target_notification):
        # Pre django code
        match = []
        tags_string = target_notification.getTags()
        filter_elements =  tags_string.split(',')
        for device in Device.objects.enabled():
            add_to_match = True
            for elem in filter_elements:
                if elem not in device.getTags():
                    add_to_match = False
                    break
            if add_to_match:
                match.append(device)
        return match
    
class Device(models.Model):
    uuid = models.CharField(max_length=32, primary_key=True)
    token = models.CharField(max_length=250)
    tags = models.TextField()
    enabled = models.BooleanField(default=True)
        
    def disableNotifications(self):
        self.enabled = False
        self.save()

    def setTags(self, tag_string):
        self.tags = tag_string
        self.save()

    def setStatus(self, status):
        self.enabled = status
        self.save()
        
    def getTags(self):
        return self.tags

    def getToken(self):
        return self.token

    def getUuid(self):
        return self.uuid
    
    objects = DeviceManager()
    
class Notification(models.Model):
    title = models.CharField(max_length=50)
    extra_context = models.TextField(blank=True, null=True)
    tags = models.TextField(blank=True, null=True)
    sent = models.BooleanField(default=False)
    data = models.DateTimeField(auto_now_add=True)
    
    def getTitle(self):
        return self.title

    def setTags(self, tag_string):
        self.tag = tag_string
        self.save()
        
    def getTags(self):
        return self.tags

    def getTargetDevices(self):
        return []

    def setSent(self):
        self.sent = True
        self.save()
        
    def isSent(self):
        return self.sent

    def getData(self):
        return self.data

    def getExtra(self):
        return self.extra_context or {}
    
    def send(self):
        if self.isSent() is False:
            devices_token = set()
            devices = Device.objects.search(self)
            for device in devices:
                devices_token.add(device.getToken())
            status = send_request(list(devices_token), self)
            if status is True:
                self.setSent()

    def save(self, *args, **kwargs):
        super(Notification, self).save(*args, **kwargs)
        self.send()
