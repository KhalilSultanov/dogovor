from django.shortcuts import redirect

class AuthRequiredMiddleware:
    """
    Middleware, которая перенаправляет неаутентифицированных пользователей на страницу входа
    при попытке доступа к URL, начинающимся с '/main/'.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/main/') and not request.session.get('authenticated'):
            return redirect('login')
        response = self.get_response(request)
        return response
