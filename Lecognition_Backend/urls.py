from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [ 
    path('api/user/all',views.user_all_api), # GET all
    path('api/user/<int:id>', views.user_api),
    path('api/user', views.user_api),
    path('api/scan/user/',views.user_scans_api),
    path('api/scan/tree/<int:id>',views.tree_scans_api),
    path('api/scan/<int:id>',views.scan_api),
    path('api/scan',views.scan_api), # GET all
    path('api/tree/<int:id>',views.tree_api),
    path('api/tree',views.tree_api),
    path('api/disease/<int:id>', views.disease_api),
    path('api/disease',views.disease_api), # GET all
    path('api/bookmark/user/',views.user_bookmark_api),
    path('api/bookmark/<int:id>',views.bookmark_api),
    path('api/bookmark',views.bookmark_api), # GET all
    path('api/register',views.register),
    path('api/login', views.login),
    # Untuk Mobile, Token harap selalu dicek di client side
    # Jika access token expired, bisa di refresh dengan refresh token dan dapat refresh token baru
    # Jika refresh token juga expired, token refresh bakal return error 401 atau unauthorized dan client side harus logout
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns = format_suffix_patterns(urlpatterns)