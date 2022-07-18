from authentication import views
from django.urls import path

app_name = 'auth'

urlpatterns = [
    path(
        'signup/',
        views.CreateUserViewSet.as_view({'post': 'create'}),
        name='create-user'
    ),
    path('token/', views.get_token, name='get-token'),
]
