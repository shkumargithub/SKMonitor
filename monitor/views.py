from django.http import HttpResponse
from django.template import loader
from SKLibPY.FileSystem.FileSystem import SKFileSystem

# Create your views here.

from monitor.models import FSList


def index(request):
    return HttpResponse("Hello, this is monitoring apps index")


def machine(request):
    latest_machine_list = FSList.objects.order_by('sno')[:5]
    template = loader.get_template('machine.html')

    system_usage1 = SKFileSystem().checkFSUsageLocal("/")
    # system_usage = " 4 "
    context = {
        'latest_machine_list': latest_machine_list,
        'system_usage': system_usage1
    }
    return HttpResponse(template.render(context, request))


def machinedetails(request, sno):
    return HttpResponse("You are looking for machine : " + str(sno))


def dashboard(request):
    title = "Monitoring Dashboard"
    latest_machine_list = FSList.objects.order_by('sno')[:5]
    template = loader.get_template('dashboard.html')
    context = {
        'title': title,
        'latest_machine_list': latest_machine_list,
    }
    return HttpResponse(template.render(context, request))
