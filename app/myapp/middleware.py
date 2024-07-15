# middleware.py

from django.shortcuts import redirect

class SessionCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if 'email' in request.session and 'code' in request.session:
            if not request.path in ['/home/', '/logout/']:
                return redirect('home')

        # Code to be executed for each request/response after
        # the view is called.
        response = self.get_response(request)
        return response