from django.urls import path

from authentication import views

app_name = 'auth'

urlpatterns = [
    path(
        'signup/',
        views.CreateUserViewSet.as_view({'post': 'create'}),
        name='create-user'
    ),
    path('token/', views.get_token, name='get-token'),
]
