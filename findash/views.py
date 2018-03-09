from django.http import HttpResponse
import datetime

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now {}.</body></html>".format(now)
    return HttpResponse(html)


def hours_ahead(request, offset):
    offset = int(offset) # it is input as a string
    # add offset hours to now
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)

    html = "<html><body>In {} hours, it will be {}.</body></html>".format(offset, dt)

    return HttpResponse(html)
