from django.db import models


class User(models.Model):

    username = models.CharField(max_length=255,null=False, blank=False)
    age = models.IntegerField(null=False, blank=False)
    email = models.EmailField(max_length=255,null=False, blank=False)
    password = models.CharField(max_length=255,null=False, blank=False)


class SearchResult(models.Model):

    user_query = models.CharField(max_length=255)  
    response_list = models.JSONField()
