from django.shortcuts import render
from skillcorner_opendata.models import Match

# Create your views here.
def index(request):
    matches = Match.objects.all()
    return render(request, 'skillcorner_opendata/index.html', {'matches': matches})