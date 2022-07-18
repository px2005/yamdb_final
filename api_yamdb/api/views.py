from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.response import Response

from .filters import TitleFilter
from .mixins import CreateListDestroyMixin
from .permissions import (IsAdmin, IsMeAndSuperUserAndAdmin,
                          ReadOnly, ReadOnlyOrAuthorModeratorAdmin,)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleCreateSerializer, TitleSerializer,
                          UserSerializer,)
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import UserProfile


class CategoryViewSet(CreateListDestroyMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = ((IsAdmin | ReadOnly),)
    lookup_field = 'slug'


class GenreViewSet(CategoryViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).all().order_by('name')
    permission_classes = ((IsAdmin | ReadOnly),)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitleCreateSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (ReadOnlyOrAuthorModeratorAdmin,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return Review.objects.filter(title=title)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (ReadOnlyOrAuthorModeratorAdmin,)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsMeAndSuperUserAndAdmin,)
    search_fields = '=user__username'
    lookup_field = 'username'

    def get_object(self):
        if self.kwargs.get('username') == 'me':
            username = self.request.user
        else:
            username = self.kwargs.get('username')
        obj = get_object_or_404(UserProfile, username=username)
        self.check_object_permissions(self.request, obj)
        return obj

    def destroy(self, request, *args, **kwargs):
        if self.kwargs.get('username') == 'me':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
