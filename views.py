from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from .models import Teacher, SDClass

def index(request):
    return render(request, 'siteScrape/index.html')
def about(request):
    return render(request, 'siteScrape/about.html')

def results(request):

    #First get all the class names as an array.
    classArray = request.GET.get('classes').split(",")
    passedArray = []
    allClassList = SDClass.objects

    for nameIndex in range(len(classArray)):

        if allClassList.filter(title=classArray[nameIndex].strip().upper()).exists():

            passedArray.append(allClassList.filter(title=classArray[nameIndex].strip().upper())[0])

    return render(request, 'siteScrape/results.html', {'classes': passedArray})

