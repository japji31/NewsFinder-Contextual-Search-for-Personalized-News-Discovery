from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .serializers import UserSerializer
from .searching import SearchNews
from .models import SearchResult,User
from dotenv import load_dotenv
import os
from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .task import add_data,embedding_create


def user_signup(request):

    if request.method=='POST':
        uname=request.POST.get('username')
        age = int(request.POST.get('age'))
        email=request.POST.get('email')
        pass1=request.POST.get('password')

        serializer = UserSerializer(data={
            'username': uname,
            'age': age,
            'email': email,
            'password': pass1
        })
        if serializer.is_valid():  
            serializer.save()
            return redirect('login') 
        else:
            return render(request, 'signup.html', {'errors': serializer.errors})
    else:
        return render(request, 'signup.html')

def user_login(request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                login(request,user)
                return redirect('user_ml')
            else:
                return HttpResponse ("Username or Password is incorrect!!!")
        else:
            return render (request,'login.html')

@login_required(login_url='login')  
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
        
        return JsonResponse(response_data)
    return render(request, 'news.html')


def cron(request):
    add_data.delay()
    embedding_create.delay()
    return HttpResponse("DONE")