from django.db import models

class SearchResult(models.Model):
    user_query = models.CharField(max_length=255)  
    response_list = models.JSONField()
  
    def __str__(self):
        return f"User Query: {self.user_query}"
