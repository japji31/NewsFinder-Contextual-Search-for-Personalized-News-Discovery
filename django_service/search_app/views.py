from django.http import JsonResponse
from django.views.decorators.http import require_POST   
from django.views.decorators.csrf import csrf_exempt
from .searching import SearchNews
from .models import SearchResult
from dotenv import load_dotenv
import os
@csrf_exempt
@require_POST
def context_search(request):
    # Extract user query from the POST request data
    user_query = request.POST.get('user_query')
    load_dotenv()
    connection_string = os.getenv('connection_string')
    search_news = SearchNews(connection_string)

    # Generate embedding for user query
    user_embedding = search_news.generate_embedding(user_query)

    # Retrieve top similar news items
    top_news = search_news.retrieve_top_news(user_embedding)

    # Prepare the response data
    response_data = {
        "user_query": user_query,
        "similar_news": top_news
    }

    search_result = SearchResult.objects.create(
        user_query=user_query,
        response_list=top_news  
    )

    # Return the response as JSON
    return JsonResponse(response_data)
