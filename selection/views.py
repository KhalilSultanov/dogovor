from django.shortcuts import render, redirect

from django.shortcuts import render


class SessionAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/main/') and not request.session.get('authenticated'):
            return redirect('/')
        return self.get_response(request)


def index(request):
    return render(request, 'index.html')
