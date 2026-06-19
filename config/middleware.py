import logging

logger = logging.getLogger(__name__)

class AccessDeniedLoggingMiddleware:
  def __init__(self, get_response):
    self.get_response = (get_response)

  def __call__(self, request):
    response = self.get_response(request)

    if response.status_code == 403:
      logger.warning(
        (
          f'403 Forbidden | '
          f'User={request.user} | '
          f'Path={request.path}'
        )
      )

    return response