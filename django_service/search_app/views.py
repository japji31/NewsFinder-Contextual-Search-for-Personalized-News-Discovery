from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .searching import SearchNews
from .models import SearchResult
from dotenv import load_dotenv
import os
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required

# @login_required(login_url='login')

def user_signup(request):

    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:
            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')

    return render (request,'signup.html')

     
def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('news')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def user_ml(request):
    if request.method == 'POST':
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

    else:
        return render(request, 'news.html')
@csrf_exempt
def context_search(request):
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

    return JsonResponse(response_data)
