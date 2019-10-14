from django.urls import path


from .views import UserProfileRudView, UserProfileAPIView
app_name = 'postings'

urlpatterns = [
    path('', UserProfileAPIView.as_view(), name='post-listcreate'),
    path('<int:pk>/', UserProfileRudView.as_view(), name='post-rud')
]   