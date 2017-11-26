from django.conf.urls import url
from .views import ProfileDetailView

urlpatterns = [
    url(r'^(?P<username>[\w-]+)/$', ProfileDetailView.as_view(template_name='profiles/user.html'), name='detail'),
    # url(r'^(?P<username>.+)/$', ProfileDetailView.as_view(), name='username')
]

