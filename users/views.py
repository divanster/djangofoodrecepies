from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Avg
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from star_ratings.models import Rating

from food.models import Item
from .forms import RegisterForm


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'users/register.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        messages.success(self.request, f'Welcome {username}, your account has been created!')
        return response

    def get_success_url(self):
        return reverse_lazy('login')


class ProfilePageView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.get_object()
        items = Item.objects.filter(user_name=profile_user)
        for item in items:
            ratings = Rating.objects.filter(content_type__model='item', object_id=item.id)
            item.average_rating = ratings.aggregate(Avg('average'))['average__avg'] or 0
            item.rating_count = ratings.count()
            user_rating = ratings.filter(user_ratings__user=self.request.user).first()
            item.user_rating = user_rating.average if user_rating else None
        context['items'] = items
        return context


@login_required
def logout_view(request):
    logout(request)
    return redirect('index')
