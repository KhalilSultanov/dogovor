from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
import logging

logger = logging.getLogger(__name__)


@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        logger.info('Login attempt: username=%s', username)

        if username == "yourUsername" and password == "yourPassword":
            request.session['authenticated'] = True  # Сохраняем флаг аутентификации в сессии
            logger.info('Login successful for username=%s', username)
            return JsonResponse({"success": True})
        else:
            logger.warning('Login failed for username=%s', username)
            return JsonResponse({"success": False, "error": "Неверные данные!"}, status=401)

    if request.session.get('authenticated'):
        logger.info('User already authenticated, redirecting to /main/')
        return redirect('/main/')  # Если уже аутентифицирован, перенаправляем на /main/

    logger.info('Rendering login page')
    return render(request, 'login.html')
