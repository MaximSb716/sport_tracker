from django.contrib.auth import login, authenticate, logout
from django.contrib.messages import constants as messages
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from main.forms import SignInForm, SignUpForm, NewVotingForm
from main.models import Votings, Questions, Answers
# Create your views here.

def index1(request):
    context = {"is_admin": False}
    if request.user.is_superuser:
        context["is_admin"] = True
    return render(request, 'index1.html', context)

def about_us(request):
    context = {"is_admin": False}
    if request.user.is_superuser:
        context["is_admin"] = True
    return render(request, 'about_us.html', context)

def catalog(request):
    categories = Votings.objects.all()
    context = {"is_admin": False,
               "categories": categories
    }
    if request.user.is_superuser:
        context["is_admin"] = True
    return render(request, 'catalog.html', context)

def profile(request):
    context = {
        "is_admin": False,
        "is_auth": False
    }
    if request.user.is_superuser:
        context["is_admin"] = True
    if request.user.is_authenticated:
        context["is_auth"] = True
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
            return redirect("/")
    else:
        form = SignUpForm()

    context = {
        "is_admin": False,
        "form": form
    }
    if request.user.is_superuser:
        context["is_admin"] = True
    return render(request, "accounts/sign_up.html", context)


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
        form = SignInForm()
    context = {
        "is_admin": False,
        "form": form
    }
    if request.user.is_superuser:
        context["is_admin"] = True
    return render(request, "accounts/sign_in.html", context)


def sign_out(request):
    """Выход пользователя из системы."""
    logout(request)
    return redirect("/")

def votings(request):
    context = {"is_admin": False}
    if request.user.is_superuser:
        context["is_admin"] = True
    if str(request.user) == "AnonymousUser" and False:
        page = "votings_anon.html"
    else:
        page = "votings.html"

    context = {}
    return render(request, page, context)

def new_voting(request):
    context = {
        "is_admin": False,
        "is_auth": False
    }
    if request.user.is_superuser:
        context["is_admin"] = True
    if request.user.is_authenticated:
        context["is_auth"] = True
        if request.method == "POST":
            form = NewVotingForm(request.POST)
            if form.is_valid():
                print("VALID +", form.cleaned_data)
                data = form.cleaned_data
                voting = Votings(
                    author=request.user,
                    name=data.get("about_label"),
                    description=data.get("about_description"),
                    questions_number=data.get("questions_count")
                )
                voting.save()
                for i in range(int(data.get("questions_count"))):
                    question = Questions(
                        voting=voting,
                        question=data.get(f"question{i}"),
                        type_of_voting=data.get(f"type_question{i}")
                    )
                    question.save()
                    for j in range(int(data.get(f"options_count{i}"))):
                        answer = Answers(
                            question=question,
                            answer=data.get(f"option{i}_{j}")
                        )
                        answer.save()

                return redirect(f"/voting?id={voting.id}")
            else:
                print("INVALID")
        else:
            context["form"] = NewVotingForm()


    return render(request, "new_voting.html", context)

def voting(request):
    context = {
        "is_admin": False,
        "is_auth": False,
        "IsExist": False
    }
    if request.user.is_superuser:
        context["is_admin"] = True
    
    id_of_page = request.GET.get("id", "not founded")
    if (id_of_page != "not founded"):
        _voting = Votings.objects.filter(id=id_of_page)
        if (len(_voting) != 0):
            context["IsExist"] = True
            context["about_label"] = _voting[0].name
            context["about_description"] = _voting[0].description
            context["author"] = _voting[0].author
            _questions = Questions.objects.filter(voting=_voting[0])
            data = []
            i = 0
            for quest in _questions:
                i += 1
                data.append({"questions" : quest, "answers" : Answers.objects.filter(question=quest)})
            
            context["data"] = data
        else:
            print("Not Founded")
    else:
        return redirect("/catalog/")

    return render(request, 'voting.html', context)

def about_voting(request):
    context = {}

    return render(request, 'about_voting.html', context)



def survey(request):
    context = {}
    return render(request, 'survey.html', context)