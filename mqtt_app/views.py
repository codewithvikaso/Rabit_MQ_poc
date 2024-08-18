from django.http import JsonResponse, HttpResponseBadRequest
from pymongo import MongoClient
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

# MongoDB setup
MONGO_URI = 'mongodb://localhost:27017/'
MONGO_DB = 'mqtt_db'
MONGO_COLLECTION = 'status_data'

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

@method_decorator(csrf_exempt, name='dispatch')
class StatusCountView(View):
    def get(self, request):
        # Get start_time and end_time from the request
        start_time = request.GET.get('start_time')
        end_time = request.GET.get('end_time')

        # Validate that start_time and end_time are provided
        if start_time is None or end_time is None:
            return HttpResponseBadRequest("Missing 'start_time' or 'end_time' parameter")

        try:
            # Convert to float
            start_time = float(start_time)
            end_time = float(end_time)
        except ValueError:
            return HttpResponseBadRequest("Invalid 'start_time' or 'end_time' parameter. They must be numbers.")

        # MongoDB aggregation pipeline
        pipeline = [
            {"$match": {"timestamp": {"$gte": start_time, "$lte": end_time}}},
            {"$group": {"_id": "$status", "count": {"$sum": 1}}}
        ]

        # Execute the aggregation
        result = list(collection.aggregate(pipeline))
        return JsonResponse(result, safe=False)
