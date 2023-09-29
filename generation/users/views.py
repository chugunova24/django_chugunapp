from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.urls import reverse

from django.views.decorators.cache import cache_page

from .mixins import DataMixin
from .forms import *
from .models import *
from .mixins import *

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.views.generic import ListView
from django.views.generic.edit import FormView
# from django.template import RequestContext # устарел
from django.forms.models import model_to_dict


class RegisterUserView(DataMixin, CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login') # после он должен повторить

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация") # для менюшки в html


        # context['user'] = model_to_dict(self.request.user)
        context = context | c_def
        # context['user'] = self.request.user.username
        return context

class LoginUserView(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('profile')


def logout_user(request):
    logout(request)
    return redirect('login')


@method_decorator(login_required, name='dispatch')
class ProfileView(UpdateView):
    model = Profile
    template_name = "users/profile.html"
    context_object_name = 'form'
    form_class = ProfileUpdateForm
    object = None
    queryset = None

    def get_queryset(self, *args, **kwargs):
        self.queryset = Profile.objects.select_related("country", "city").get(user=self.request.user)
        return self.queryset

    def get_object(self, queryset=None, *args, **kwargs):
        queryset = self.get_queryset()
        self.object = self.queryset

        return self.object

    def form_valid(self, form):

        for fieldname in form.changed_data:
            old_profile = self.object

            if fieldname == 'image' and old_profile.image:
                default_image = os.path.join(MEDIA_ROOT, self.object.default_image)
                old_image_path = old_profile.image.path

                if os.path.exists(old_image_path) and (old_image_path != default_image):
                    os.remove(old_image_path)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('profile')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        image_data = data['form']['image']

        if image_data.initial == self.model.default_image:
            image_data.default_image = True
        else:
            image_data.default_image = False

        return data

