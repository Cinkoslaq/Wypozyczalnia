
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View

from Wyporzyczalnia_app.forms import AddUserForm, LoginUserForm, AddMachineryForm
from Wyporzyczalnia_app.models import Machinery, Rental, Company, Ratings, Comments

def home(request):
    return render(request, 'home.html')

def uslugi(request):
    opis_uslug = "Główne usługi naszego portalu to wypożyczanie maszyn budowlanych, rolniczych oraz transportu w razie przeprowadzki. Nie kupuj, lepiej wypożycz!"
    return render(request, 'uslugi.html', {'opis_uslug': opis_uslug})

def onas(request):
    komunikat = "Witamy, jesteśmy nowi na rynku i stworzyliśmy tę aplikację głównie do wypożyczania, aby nie kupować i nie przepłacać."
    return render(request, 'onas.html', {'komunikat': komunikat})

def machinery_list(request):
    machinery_items = Machinery.objects.all()
    return render(request, 'machinery_list.html', {'machinery_items': machinery_items})

def machinery_detail(request, machinery_id):
    machinery = get_object_or_404(Machinery, pk=machinery_id)
    return render(request, 'machinery_detail.html', {'machinery': machinery})

def rental_list(request):
    rental_items = Rental.objects.all()
    return render(request, 'rental_list.html', {'rental_items': rental_items})

def rental_detail(request, rental_id):
    rental = get_object_or_404(Rental, pk=rental_id)
    return render(request, 'rental_detail.html', {'rental': rental})

def company_detail(request, company_id):
    company = get_object_or_404(Company, pk=company_id)
    ratings = Ratings.objects.filter(company=company)
    comments = Comments.objects.filter(company=company)
    return render(request, 'company_detail.html', {'company': company, 'ratings': ratings, 'comments': comments})

def add_rating(request, company_id):
    if request.method == 'POST':
        rating_value = request.POST['rating']
        company = get_object_or_404(Company, pk=company_id)
        Ratings.objects.create(company=company, rating=rating_value)
        return HttpResponseRedirect(reverse('company_detail', args=(company_id,)))
    else:
        return render(request, 'add_rating.html')

def add_comment(request, company_id):
    if request.method == 'POST':
        comment_content = request.POST['comment']
        company = get_object_or_404(Company, pk=company_id)
        Comments.objects.create(company=company, content=comment_content)
        return HttpResponseRedirect(reverse('company_detail', args=(company_id,)))
    else:
        return render(request, 'add_comment.html')


def add_machinery(request):
    if request.method == 'POST':
        form = AddMachineryForm(request.POST)
        if form.is_valid():
            machinery = form.save()
            return redirect('machinery_detail', machinery_id=machinery.id)
    else:
        form = AddMachineryForm()

    return render(request, 'add_machinery.html', {'form': form})

class LoginUser(View):
    def get(self, request):
        form = LoginUserForm()
        return render(request, 'login_user.html', {'form': form})
    def post(self, request):
        form = LoginUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                message = 'Udało się zalogować' + request.user.username
                ctx = {
                    'message': message,
                    'form': form,
                }
                return render(request, 'login_user.html', context=ctx)
            else:
                message = 'Nie udało się zalogować! :('
                ctx = {
                    'message': message,
                    'form': form,
                }
                return render(request, 'login_user.html', context=ctx)

class LogoutUser(View):
    def get(self, request):
        logout(request)
        message = 'Użytkownik wylogowany, zaloguj ponownie!'
        ctx = {
            'message': message,
        }
        return render(request, 'logout_user.html', context=ctx)

class AddUser(View):
    def get(self, request):
        form = AddUserForm()
        return render(request, 'add_user.html', {'form': form})

    def post(self, request):
        form = AddUserForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data['login']
            password = form.cleaned_data['password']
            rep_password = form.cleaned_data['rep_pass']
            name = form.cleaned_data['name']
            lastname = form.cleaned_data['lastname']
            mail = form.cleaned_data['mail']
            try:
                user = User.objects.get(username=login)
            except User.DoesNotExist:
                user = None
            if user is not None:
                mass = 'Login użytkownika istnieje spróbuj ponownie'
                ctx = {
                    'message': mass,
                    'form': form,
                }
                return render(request, 'add_user.html', context=ctx)
            else:
                if password == rep_password:
                    user_stop = User.objects.create_user(username= login, first_name=name, last_name=lastname, email=mail, password=password )
                    mass = 'Użytkownik ' + login + ' został dodany!.'
                    ctx = {
                        'message': mass,
                        'form': form,
                    }
                    return render(request, 'add_user.html', context=ctx)
                else:
                    mass = 'Hasło się nie zgadza!'
                    ctx = {
                        'message': mass,
                        'form': form,
                    }
                    return render(request, 'add_user.html', context=ctx)

