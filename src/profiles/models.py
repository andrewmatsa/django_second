from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from .utils import code_generator
from django.dispatch import receiver

User = settings.AUTH_USER_MODEL


# class ProfileManager(models.Manager):
#     def toggle_follow(self, request_user, username_to_toggle):
#         profile_ = Profile.objects.get(user__username__iexact=username_to_toggle)
#         user = request_user
#         is_following = False
#         if user in profile_.followers.all():
#             profile_.followers.remove(user)
#         else:
#             profile_.followers.add(user)
#             is_following = True
#         return profile_, is_following

class Profile(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number    = models.CharField(max_length=15, blank=True, null=False)
    activated       = models.BooleanField(default=False)
    activation_key  = models.CharField(max_length=120, blank=True, null=True)
    timestamp       = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)

    # object = ProfileManager()

    def __str__(self):
        return self.user.username

    def send_activation_email(self):
        if not self.activated:
            self.activation_key = code_generator()
            self.save()
            path_ = reverse('activate', kwargs={"code": self.activation_key})
            subject = "Activate Account"
            from_mail = settings.DEFAULT_FROM_EMAIL
            message = 'Activate your account here: %s' % path_
            recipient_list = [self.user.email]
            html_message = '<p>Activate your account here: %s</p>' % path_
            sent_mail = send_mail(subject,
                                  message,
                                  from_mail,
                                  recipient_list,
                                  fail_silently=False,
                                  html_message=html_message)
            sent_mail = True
            return sent_mail

    def get_phone_number(self):
        return self.phone_number.strip()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# def post_save_user_receiver(sender, instance, created, *args, **kwargs):
#     if created:
#         profile, is_created =Profile.objects.get_or_create(user=instance)
#
#
# post_save.connect(post_save_user_receiver, sender=User)