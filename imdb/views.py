import os
from django.http import HttpResponse, JsonResponse
from web_scrapper.helpers import send_request
from .core.extract_info import top_chart_extraction

def weekly_top(request):
    try:
        url = os.getenv('IMDB_CHART_TOP')
        response = send_request.request_web_page(url)
        if response is not None:
            top_movies_list = top_chart_extraction(response=response)
            return JsonResponse(top_movies_list,safe=False)
        else:
            return HttpResponse("Failed to fetch top movies list", status=500)
    except Exception as e:
        print(f"Exception occured: {e}")