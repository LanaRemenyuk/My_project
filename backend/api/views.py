from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from .filters import MaterialFilter
from materials.models import Tag, Follow, Material
from rest_framework import status, viewsets
from rest_framework.decorators import action
from .serializers import (CustomUserSerializer, TagSerializer,
                          FollowSerializer, MaterialSerializer)

from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from users.models import CustomUser
from .paginators import PageLimitPagination
from .permissions import IsAuthorAdminOrReadOnly


class CustomUserViewSet(UserViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        queryset = CustomUser.objects.filter(followed__user=request.user)
        if queryset:
            pages = self.paginate_queryset(queryset)
            serializer = FollowSerializer(pages, many=True,
                                          context={'request': request})
            return self.get_paginated_response(serializer.data)
        return Response('У Вас нет подписок.',
                        status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=('post',),
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(CustomUser, id=id)
        subscription = Follow.objects.filter(
            user=user.id, author=author.id
        )
        if user == author:
            return Response('Упс! Нельзя подписаться на самого себя!',
                            status=status.HTTP_400_BAD_REQUEST)
        if subscription.exists():
            return Response(f'Вы уже подписаны на {author}',
                            status=status.HTTP_400_BAD_REQUEST)
        subscribe = Follow.objects.create(
            user=user,
            author=author
        )
        subscribe.save()
        return Response(f'Вы подписались на {author}',
                        status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(CustomUser, id=id)
        change_subscription = Follow.objects.filter(
            user=user.id, author=author.id
        )
        change_subscription.delete()
        return Response(f'Подписка на {author} удалена',
                        status=status.HTTP_204_NO_CONTENT)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class MaterialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    permission_classes = (IsAuthorAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MaterialFilter
    pagination_class = PageLimitPagination