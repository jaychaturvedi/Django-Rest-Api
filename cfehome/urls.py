
from django.urls import path, include
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    # url(r'^api/auth/login/$', obtain_jwt_token, name='api-login'),
    # url(r'^api/postings/', include('postings.api.urls', namespace='api-postings')),
    path('admin/', admin.site.urls),
    path('api/auth/login/', obtain_jwt_token, name='api-login'),
    path('api/postings/', include('postings.api.urls', namespace = "api-postings")), #  , namespace='api-postings'
]

