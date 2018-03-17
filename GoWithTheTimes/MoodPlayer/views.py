from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def PlayerService(request):
    skip = request.GET['skip']
    result = ''
    if(skip == '1'):
        result = "skipped"
    else:
        result = "keep playing"
    return HttpResponse(result)
