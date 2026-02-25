from django.contrib import admin
from .models import CustomUser, Course, Note, Meeting, StudySession, Notification, Message

admin.site.register(CustomUser)
admin.site.register(Course)
admin.site.register(Note)
admin.site.register(Meeting)
admin.site.register(StudySession)
admin.site.register(Notification)
admin.site.register(Message)