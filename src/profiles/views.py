from django.contrib.auth import get_user_model, get_user
from django.http import Http404
from django.http import request
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import BaseDetailView

from .forms import RegisterForm
from .models import Profile
User = get_user_model()


def activate_user_view(request, code=None, *args, **kwargs):
    if code:
        qs = Profile.objects.filter(activation_key=code)
        if qs.exists() and qs.count() == 1:
            profile = qs.first()
            if not profile.activated:
                user_ = profile.user
                user_.is_active = True
                user_.save()
                profile.activated = True
                profile.activation_key = None
                profile.save()
                return redirect("/login")
    return redirect("/login")


class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'registration/login.html', context=None)


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = '/login/'

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return redirect('/logout')
        return super(RegisterView, self).dispatch(*args, **kwargs)


# class ProfileDetailView(DetailView):
#     def get_object(self):
#         username = self.kwargs.get("username")
#         if username is None:
#             raise Http404
#         return get_object_or_404(User, username__iexact=username, is_active=True)


def view_profile(request):
    # if pk:
    #     user = User.objects.get(pk=pk)
    # else:
    #     user = request.user
    args = {'user': request.user}
    return render(request, 'profiles/user.html', args)
