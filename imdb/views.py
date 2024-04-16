import os
import json
from django.views.decorators.http import require_POST,require_http_methods
from django.http import HttpResponse, JsonResponse
from web_scrapper.helpers import send_request
from .core.extract_info import top_chart_extraction, upcoming_releases_extract
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token


@require_http_methods(['GET'])
def weekly_top(request):
    try:
        url = os.getenv("IMDB_CHART_TOP")
        response = send_request.request_web_page(url)
        if response is not None:
            top_movies_list = top_chart_extraction(response=response)
            return JsonResponse(top_movies_list,safe=False)
        else:
            return HttpResponse("Failed to fetch top movies list", status=500)
    except Exception as e:
        print(f"Exception occured: {e}")


@csrf_exempt
@require_http_methods(['POST'])
def upcoming_releases(request):
    try:
        request_body = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse("Invalid Json")
    
    query_type = request_body.get("type").upper() # type of content (MOVIE/TV/TV_EPISODE)
    query_region_name = request_body.get("region")
    with open('web_scrapper\country_codes.json') as f:
        region_code = json.load(f)
    query_region_code = region_code.get(query_region_name) if region_code.get(query_region_name) else "" # country code for building url (default:United States)
    try:
        base_url = os.getenv("IMDB_UPCOMING_RELEASES_CALENDER")
        url = base_url + f"?region={query_region_code}&type={query_type}"
        response = send_request.request_web_page(url)
        if response is not None:
            upcoming_releases_list = upcoming_releases_extract(response=response)
            return JsonResponse(upcoming_releases_list,safe=False)
        else:
            return HttpResponse("Failed to fetch upcoming movies list", status=500)
        
    except Exception as e:
        print(f"Exception occured: {e}")