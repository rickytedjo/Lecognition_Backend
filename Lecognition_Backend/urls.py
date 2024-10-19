from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    path('api/user/<int:id>', views.user_api),
    path('api/user',views.user_api), # GET all
    path('api/scan/<int:id>',views.scan_api),
    path('api/scan',views.scan_api), # GET all
    path('api/disease/<int:id>', views.disease_api),
    path('api/disease',views.disease_api), # GET all
    path('api/bookmark/<int:id>',views.bookmark_api),
    path('api/bookmark',views.bookmark_api), # GET all
]

urlpatterns = format_suffix_patterns(urlpatterns)