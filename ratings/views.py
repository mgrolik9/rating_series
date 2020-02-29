
from django.views import View
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg


from rest_framework.exceptions import APIException
import requests


from ratings.models import Show, Ratings, Recommendations
from ratings.forms import LoginForm, RegisterForm, SearchShowForm, RateForm
from series_rating.local_settings import apikey


# Create your views here.

class MainPage(View):

    def get(self, request):
        return render(request, 'main.html')

    def post(self, request):
        if 'login' in request.POST:
            reverse = 'login'
        elif 'register' in request.POST:
            reverse = 'register'
        return redirect(reverse_lazy(reverse))


class LoginView(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', locals())

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(username=form.cleaned_data['login'],
                                password=form.cleaned_data['password'])

            if user is not None:
                login(request, user)
                return redirect(reverse_lazy('home'))

            else:
                response = 'Nie ma takiego użytkownika.'
                return render(request, 'login.html', {'form': form,
                                                      'response': response})


class RegisterView(View):

    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', locals())

    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():

            login = form.cleaned_data['login']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            second_password = form.cleaned_data['second_password']
            user_check = User.objects.filter(username=login)
            user_check_2 = User.objects.filter(email=email)

            if user_check:
                response = 'Podany użytkownik już istnieje'
            elif user_check_2:
                response = 'Podany email już istnieje'
            elif password != second_password:
                response = 'Hasło się nie zgadza'
            else:
                User.objects.create_user(username=login,
                                         password=password,
                                         email=email)
                return redirect(reverse_lazy('login'))

            return render(request, 'register.html', {'form': form,
                                                     'response': response})


class UserLogout(View):

    def get(self, request):
        logout(request)
        return redirect(reverse_lazy('main-page'))


class HomeView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        form = SearchShowForm()
        shows = Show.objects.all().order_by('-id')

        return render(request, 'home.html', locals())

    def post(self, request):
        form = SearchShowForm(request.POST)
        shows = Show.objects.all().order_by('-id')

        if form.is_valid():
            show = form.cleaned_data['show_title'].capitalize()
            try:
                payload = {'t': show, 'apikey': apikey}
                response = requests.get("http://www.omdbapi.com/", params=payload)
            except APIException:
                response = 'Niestety nie ma takiego serialu :('
                return render(request, 'home.html', {'form': form,
                                                     'shows': shows,
                                                     'response': response})

            json_response = response.json()
            type = json_response.get("Type")

            if type == "series":
                year = json_response.get("Year")
                add_show, created = Show.objects.get_or_create(title=show, year=year)
                return redirect(reverse_lazy('show', args=[add_show.id]))
            else:
                response = 'Niestety nie ma takiego serialu :('
                return render(request, 'home.html', {'form': form,
                                                     'shows': shows,
                                                     'response': response})


class ShowView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, show_id):
        show = Show.objects.get(pk=show_id)
        ratings = Ratings.objects.filter(show=show)

        payload = {'t': show.title, 'apikey': apikey}
        response = requests.get("http://www.omdbapi.com/", params=payload)
        json_response = response.json()
        poster = json_response.get("Poster")

        return render(request, 'show.html', {'show': show,
                                             'ratings': ratings,
                                             'poster': poster})


class RateView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, show_id):
        form = RateForm()
        show = Show.objects.get(pk=show_id)

        payload = {'t': show.title, 'apikey': apikey}
        response = requests.get("http://www.omdbapi.com/", params=payload)
        json_response = response.json()
        poster = json_response.get("Poster")

        return render(request, 'rate.html', {'form': form,
                                             'show': show,
                                             'poster': poster})

    def post(self, request, show_id):
        form = RateForm(request.POST)
        show = Show.objects.get(pk=show_id)

        if form.is_valid():
            try:
                rate = Ratings.objects.get(show=show, user=request.user)
            except ObjectDoesNotExist:
                new_rate = Ratings.objects.create(show=show, user=request.user,
                                                  rating=form.cleaned_data['rating'],
                                                  comment=form.cleaned_data['comment'])
                new_rate.save()

                if form.cleaned_data['recommend'] == '1':
                    new_recommend, created = Recommendations.objects.get_or_create(user=request.user)
                    new_recommend.shows.add(show)
                    return redirect(reverse_lazy('profile'))
                return redirect(reverse_lazy('show', args=[show.id]))

            rate.rating = form.cleaned_data['rating']
            rate.comment = form.cleaned_data['comment']
            rate.save()

            if form.cleaned_data['recommend'] == '1':
                new_recommend, created = Recommendations.objects.get_or_create(user=request.user)
                new_recommend.shows.add(show)
                return redirect(reverse_lazy('profile'))
            return redirect(reverse_lazy('show', args=[show.id]))


class ProfileView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):

        try:
            recommendations = Recommendations.objects.get(user=request.user)
            shows = Show.objects.filter(recommendations_set=recommendations.id).order_by('title')
        except ObjectDoesNotExist:
            response = 'Nie masz polecanych seriali :('
            return render(request, 'profile.html', {'response': response})

        user_recommendations = {}

        for show in shows:
            payload = {'t': show.title, 'apikey': apikey}
            response = requests.get("http://www.omdbapi.com/", params=payload)
            json_response = response.json()
            poster = json_response.get("Poster")
            user_recommendations[show] = poster

        return render(request, 'profile.html', {'user': request.user.username,
                                                'user_recommendations': user_recommendations.items()})


class DeleteView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, show_id):
        show = Show.objects.get(pk=show_id)
        recommendations = Recommendations.objects.get(user=request.user)
        recommendations.shows.remove(show)
        return redirect(reverse_lazy('profile'))


class UserProfileView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)

        if user == request.user:
            return redirect(reverse_lazy('profile'))

        try:
            recommendations = Recommendations.objects.get(user=user)
            shows = Show.objects.filter(recommendations_set=recommendations.id).order_by('title')
        except ObjectDoesNotExist:
            response = 'Ten użytkownik nie ma jeszcze polecanych seriali :('
            return render(request, 'user_profile.html', {'user': user.username,
                                                         'response': response})
        user_recommends = {}

        for show in shows:
            payload = {'t': show.title, 'apikey': apikey}
            response = requests.get("http://www.omdbapi.com/", params=payload)
            json_response = response.json()
            poster = json_response.get("Poster")
            user_recommends[show] = poster

        return render(request, 'user_profile.html', {'user': user.username,
                                                     'user_recommendations': user_recommends.items()})


class TopView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        shows = Show.objects.all().annotate(rating_avg=Avg('ratings__rating')).order_by('-rating_avg')
        return render(request, 'top.html', {'shows': shows})


