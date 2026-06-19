from rest_framework.pagination import (
  CursorPagination,
  PageNumberPagination,
)

class FeedPagination(
  CursorPagination
):
  page_size = 20
  ordering = '-created_at'

class UserPagination(
  PageNumberPagination
):
  page_size = 20
  page_query_param = 'page'

class CommentPagination(
  PageNumberPagination
):
  page_size = 20
  page_query_param = 'page'