from django.shortcuts import render

from apps.users.models import InfoUser, Services, Experience

# Create your views here.

def index(request):
    infouser = InfoUser.objects.latest("id")
    service = Services.objects.all()
    experience = Experience.objects.all().order_by("-id")
    return render(request, "index.html", locals())