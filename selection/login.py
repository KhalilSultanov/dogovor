from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if username == "yourUsername" and password == "yourPassword":
            request.session['authenticated'] = True  # Сохраняем флаг аутентификации в сессии
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "error": "Неверные данные!"})

    if request.session.get('authenticated'):
        return redirect('/main/')  # Если уже аутентифицирован, перенаправляем на /main/

    return render(request, 'login.html')
