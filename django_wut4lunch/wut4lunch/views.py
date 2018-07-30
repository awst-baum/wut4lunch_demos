from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework import permissions
from wut4lunch.serializers import LunchSerializer

from .models import Lunch

# Create your views here.
# class LunchForm(forms.Form):
#     submitter = forms.CharField(label='Your name')
#     food = forms.CharField(label='What did you eat?')
#  
# lunch_form = LunchForm(auto_id=False)
def index(request):
    lunches = Lunch.objects.all()
    context = {
        'lunches': lunches,
#         'form': lunch_form,
        }
    return render(request, 'wut4lunch/index.html', context)

def newlunch(request):
    l = Lunch()
    print(request)
    l.submitter = request.POST['submitter']
    l.food = request.POST['food']
    l.save()
    return redirect('home')

## rest views
class LunchViewSet(viewsets.ModelViewSet):    
    """
    REST API endpoint that allows lunches to be viewed or edited.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Lunch.objects.all()
    serializer_class = LunchSerializer
    