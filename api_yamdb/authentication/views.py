from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from authentication.serializers import CreateUserSerializer, GetTokenSerializer
from core.utils import get_token_for_user
from users.models import UserProfile


@api_view(['POST'])
@permission_classes([AllowAny],)
def get_token(request):
    get_token_serializer = GetTokenSerializer(data=request.data)
    if get_token_serializer.is_valid():
        username = request.data.get('username')
        user = get_object_or_404(UserProfile, username=username)
        token = get_token_for_user(user)
        return JsonResponse(token, status=status.HTTP_201_CREATED)
    return JsonResponse(
        get_token_serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


class CreateUserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK,
                        headers=headers)
