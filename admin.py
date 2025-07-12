from django.contrib import admin
from django.contrib.auth.models import User, Group

from apps.users.models import InfoUser, Services, Experience, Education

# Register your models here.
admin.site.register(InfoUser)
admin.site.register(Services)
admin.site.register(Experience)
admin.site.register(Education)

admin.site.unregister(User)
admin.site.unregister(Group)