from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView
from profiles.views import RegisterView, HomePageView, activate_user_view, view_profile

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^activate/(?P<code>[a-z0-9].*)/$', activate_user_view, name='activate'),
    # url(r'^login/$', LoginView.as_view(template_name='registration/login.html'), name='login'),
    url(r'^login/$', LoginView.as_view(template_name='registration/login.html',
                                       redirect_authenticated_user=True), name='login'),
    # url(r'^u', include('profiles.urls', namespace='account')),
    url(r'^profile/$', view_profile, name='view_profile'),

    # url(r'^profile/edit/$', ProfileDetailView.as_view(), name='edit_profile'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^home/$', HomePageView.as_view(), name='home'),
    url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^contact/$', TemplateView.as_view(template_name='contact.html'), name='contact'),
]
