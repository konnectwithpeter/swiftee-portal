from django.http import Http404
from django.conf import settings
import re

class ProtectedMediaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Compile the media URL pattern once
        self.media_url_pattern = re.compile(f'^{settings.MEDIA_URL.lstrip("/")}')

    def __call__(self, request):
        # Check if the request is for a media file
        if self.media_url_pattern.match(request.path.lstrip('/')):
            raise Http404("Direct media access is not allowed")
        return self.get_response(request)