from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from posts.models import (
  Post,
  PostMedia,
  Tag,
)

from posts.serializers import (
  PostSerializer,
  PostCreateSerializer,
)

from posts.permissions import (
  IsAuthorOrAdmin,
)

from friendships.models import (
  Follow,
)

import re

from reactions.models import Reaction

from comments.models import Comment

from comments.serializers import (
  CommentSerializer,
  CommentCreateSerializer,
)

from users.permissions import (
  IsProfilePublicOrFriend,
)

from config.pagination import (
  FeedPagination,
  CommentPagination,
)

class PostViewSet(
  viewsets.ModelViewSet
):
  pagination_class = FeedPagination

  queryset = (
    Post.objects
    .select_related('author')
    .prefetch_related(
      'medias',
      'tags',
      'comments',
      'reactions',
    )
  )

  serializer_class = PostSerializer

  def get_permissions(self):
    if self.action in [
      'create',
      'destroy',
    ]:
      return [permissions.IsAuthenticated()]

    return [permissions.AllowAny()]

  def get_serializer_class(self):
    if self.action == 'create':
      return PostCreateSerializer

    return PostSerializer

  def perform_create(
    self,
    serializer
  ):
    post = serializer.save(
      author=self.request.user
    )

    hashtags = re.findall(
      r"#(\w+)",
      post.text
    )

    for tag_name in hashtags:
      tag, _ = Tag.objects.get_or_create(
        name=tag_name.lower()
      )

      post.tags.add(tag)

    media_files = (
      self.request.FILES.getlist(
        'media_files'
      )
    )

    for file in media_files:
      media_type = (
        PostMedia.MediaType.IMAGE
      )

      if (
        file.content_type
        and file.content_type.startswith(
          'video'
        )
      ):
        media_type = (
          PostMedia.MediaType.VIDEO
        )

      PostMedia.objects.create(
        post=post,
        file=file,
        media_type=media_type,
      )

    return post

  @action(
    detail=False,
    methods=['get'],
    url_path='feed'
  )
  def feed(
    self,
    request
  ):
    queryset = Post.objects.all()

    if not request.user.is_authenticated:
        queryset = queryset.filter(
          author__is_private=False
        )

    else:
      following_ids = (
        Follow.objects
        .filter(
          follower=request.user
        )
        .values_list(
          'following_id',
          flat=True
        )
      )

      queryset = queryset.filter(
        Q(author__is_private=False)
        |
        Q(author=request.user)
        |
        Q(author_id__in=following_ids)
      ).distinct()

    page = self.paginate_queryset(queryset)

    if page is not None:
      serializer = PostSerializer(
        page,
        many=True,
        context={'request': request}
      )

      return self.get_paginated_response(
        serializer.data
      )

    serializer = PostSerializer(
      queryset,
      many=True,
      context={
        'request': request
      }
    )

    return Response(
      serializer.data
    )

  def retrieve(
    self,
    request,
    *args,
    **kwargs
  ):
    post = self.get_object()

    permission = (
      IsProfilePublicOrFriend()
    )

    if not permission.has_object_permission(
      request,
      self,
      post.author
    ):
      return Response(
        {
          'detail':
          'Perfil privado.'
        },
        status=403
      )

    serializer = PostSerializer(
      post,
      context={
        'request': request
      }
    )

    return Response(
      serializer.data
    )

  def destroy(
    self,
    request,
    *args,
    **kwargs
  ):
    post = self.get_object()

    if (
      post.author != request.user
      and request.user.role != 'ADMIN'
    ):
      return Response(
        {
          'detail':
          'Você não possui permissão.'
        },
        status=status.HTTP_403_FORBIDDEN
      )

    return super().destroy(
      request,
      *args,
      **kwargs
    )

  @action(
    detail=False,
    methods=['get'],
    url_path='search'
  )
  def search(
    self,
    request
  ):
    query = request.query_params.get(
      'q'
    )

    if not query:
      return Response([])

    posts = Post.objects.filter(
      Q(text__icontains=query)
      |
      Q(tags__name__icontains=query)
    )

    if not request.user.is_authenticated:
      posts = posts.filter(
        author__is_private=False
      )

    else:
      following_ids = (
        Follow.objects
        .filter(
          follower=request.user
        )
        .values_list(
          'following_id',
          flat=True
        )
      )

      posts = posts.filter(
        Q(author__is_private=False)
        |
        Q(author=request.user)
        |
        Q(author_id__in=following_ids)
      )
      
    posts = posts.distinct()

    page = self.paginate_queryset(posts)

    if page is not None:
      serializer = PostSerializer(
        page,
        many=True,
        context={'request': request}
      )

      return self.get_paginated_response(
        serializer.data
      )

    serializer = PostSerializer(
      posts,
      many=True,
      context={
        'request': request
      }
    )

    return Response(
      serializer.data
    )
  
  @action(
    detail=True,
    methods=['post'],
    permission_classes=[
      permissions.IsAuthenticated
    ],
    url_path='react'
  )
  def react(
    self,
    request,
    pk=None
  ):
    post = self.get_object()

    permission = (
      IsProfilePublicOrFriend()
    )

    if not permission.has_object_permission(
      request,
      self,
      post.author
    ):
      return Response(
        {
          'detail':
          'Perfil privado.'
        },
        status=status.HTTP_403_FORBIDDEN
      )

    reaction = Reaction.objects.filter(
      user=request.user,
      post=post
    ).first()

    if reaction:
      reaction.delete()
      
      return Response({
        'detail': 'Like removido.'
      })
    
    Reaction.objects.create(
      user=request.user,
      post=post
    )

    return Response({
      'detail': 'Like adicionado.'
    })
  
  @action(
    detail=True,
    methods=['get'],
    url_path='reactions'
  )
  def reactions(
    self,
    request,
    pk=None
  ):
    post = self.get_object()

    permission = (
      IsProfilePublicOrFriend()
    )

    if not permission.has_object_permission(
      request,
      self,
      post.author
    ):
      return Response(
        {
          'detail':
          'Perfil privado.'
        },
        status=status.HTTP_403_FORBIDDEN
      )

    return Response({
      'likes_count': post.reactions.count()
    })
  
  @action(
    detail=True,
    methods=['get', 'post'],
    url_path='comments',
  )
  def comments(
    self,
    request,
    pk=None
  ):
    post = self.get_object()

    permission = (
      IsProfilePublicOrFriend()
    )

    if not permission.has_object_permission(
      request,
      self,
      post.author
    ):
      return Response(
        {
          'detail':
          'Perfil privado.'
        },
        status=status.HTTP_403_FORBIDDEN
      )

    if request.method == 'GET':
      comments = (
        post.comments
        .filter(parent=None)
        .order_by('created_at')
      )

      paginator = CommentPagination()

      page = paginator.paginate_queryset(
        comments,
        request,
      )

      if page is not None:
        serializer = CommentSerializer(
          page,
          many=True
        )

        return paginator.get_paginated_response(
          serializer.data
        )
      
      serializer = CommentSerializer(
        comments,
        many=True
      )

      return Response(
        serializer.data
      )
    
    if not request.user.is_authenticated:
      return Response(
        {
          'detail':
          'Autenticação necessária.'
        },
        status=status.HTTP_401_UNAUTHORIZED
      )
    
    serializer = CommentCreateSerializer(
      data=request.data
    )

    serializer.is_valid(
      raise_exception=True
    )

    comment = serializer.save(
      post=post,
      author=request.user
    )

    return Response(
      CommentSerializer(comment).data,
      status=status.HTTP_201_CREATED
    )
  
  @action(
    detail=True,
    methods=['delete'],
    url_path=r'comments/(?P<comment_id>[^/.]+)',
    permission_classes=[
      permissions.IsAuthenticated
    ]
  )
  def delete_comment(
    self,
    request,
    pk=None,
    comment_id=None
  ):
    comment = get_object_or_404(
      Comment,
      pk=comment_id,
      post_id=pk
    )

    if (
      comment.author != request.user
      and request.user.role != 'ADMIN'
    ):
      return Response(
        {
          'detail':
          'Sem permissão.'
        },
        status=status.HTTP_403_FORBIDDEN
      )
    
    comment.delete()

    return Response(
      status=status.HTTP_204_NO_CONTENT
    )

  def create(self, request, *args, **kwargs):

    serializer = self.get_serializer(
        data=request.data
    )

    serializer.is_valid(
        raise_exception=True
    )

    post = self.perform_create(
        serializer
    )

    response_serializer = PostSerializer(
        post,
        context={
            'request': request
        }
    )

    return Response(
        response_serializer.data,
        status=status.HTTP_201_CREATED
    )