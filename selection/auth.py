from django.http import HttpResponse
from functools import wraps

from django.shortcuts import redirect


def login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.session.get('authenticated'):
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')
    return _wrapped_view
