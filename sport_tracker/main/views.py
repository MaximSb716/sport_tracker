from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import SignUpForm, SignInForm  # Импортируем наши формы

# Create your views here.

def index1(request):
    context = {}
    return render(request, 'index1.html', context)

def about_us(request):
    context = {}
    return render(request, 'about_us.html', context)

def catalog(request):
    context = {}
    return render(request, 'catalog.html', context)

def profile(request):
    context = {}
    return render(request, 'profile.html', context)

@csrf_exempt
def save_avatar(request):
    pass
    #if request.method == 'POST':
    #    data = json.loads(request.body)
    #    avatar_data = data.get('avatar')
    #    if avatar_data:
    #        # 1. Извлекаем данные base64
    #        format, imgstr = avatar_data.split(';base64,')
    #        ext = format.split('/')[-1]  # извлекаем расширение файла
    #        # 2. Декодируем base64
    #        avatar = ContentFile(base64.b64decode(imgstr), name=f'avatar.{ext}')



def sign_up(request):
    """Регистрация пользователя."""
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация прошла успешно!")
            return redirect("/")
        else:
            messages.error(request, "Ошибка регистрации. Проверьте данные.")
    else:
        form = SignUpForm()
    return render(request, "accounts/sign_up.html", {"form": form})


def sign_in(request):
    """Авторизация пользователя."""
    if request.method == "POST":
        form = SignInForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_page = request.GET.get("next")
                if next_page:
                    return redirect(next_page)
                else:
                    return redirect(
                        "/"
                    )
            else:
                messages.error(request, "Неверный логин или пароль.")
        else:
            messages.error(request, "Ошибка в форме авторизации.")
    else:
        form = SignInForm()

    return render(request, "accounts/sign_in.html", {"form": form})


def sign_out(request):
    """Выход пользователя из системы."""
    logout(request)
    messages.success(request, "Вы успешно вышли из системы.")
    return redirect("/")

