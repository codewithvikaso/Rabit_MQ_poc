from django.shortcuts import render

# Create your views here.
# mqtt_app/views.py
from django.http import JsonResponse
from django.db.models import Count
from .models import StatusMessage

def status_count(request):
    start_time = float(request.GET.get('start_time'))
    end_time = float(request.GET.get('end_time'))

    counts = StatusMessage.objects.filter(
        timestamp__gte=start_time, 
        timestamp__lte=end_time
    ).values('status').annotate(count=Count('status'))

    return JsonResponse(list(counts), safe=False)
