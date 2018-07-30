from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework import permissions
from wut4lunch.serializers import LunchSerializer

from .models import Lunch
from django.http.response import HttpResponseBadRequest, HttpResponse,\
    HttpResponseServerError
from django.utils.datastructures import MultiValueDictKeyError

# Create your views here.
# class LunchForm(forms.Form):
#     submitter = forms.CharField(label='Your name')
#     food = forms.CharField(label='What did you eat?')
#  
# lunch_form = LunchForm(auto_id=False)

## TODO: find nicer way to restrict access (not repeating login_required on every view)
@login_required(login_url='/login/')
def index(request):
    lunches = Lunch.objects.all()
    context = {
        'lunches': lunches,
#         'form': lunch_form,
        }
    return render(request, 'wut4lunch/index.html', context)

@login_required(login_url='/login/')
def newlunch(request):
    l = Lunch()
    print(request)
    try:
        l.submitter = request.POST['submitter']
        l.food = request.POST['food']
        l.save()
    except MultiValueDictKeyError as e:
        return HttpResponseBadRequest("No data given for {}".format(e))
    except Exception as ex:
        return HttpResponseServerError("Can't save: {}".format(ex))
    
    return redirect('home')

## rest views
class LunchViewSet(viewsets.ModelViewSet):    
    """
    REST API endpoint that allows lunches to be viewed or edited.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Lunch.objects.all()
    serializer_class = LunchSerializer
    