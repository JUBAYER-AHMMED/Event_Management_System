from django.db.models.signals import post_save, pre_save , post_delete, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail

# from django.contrib.auth.models import User, Group
from django.contrib.auth.models import Group

from django.contrib.auth.tokens import default_token_generator
from django.conf import settings

from users.models import CustomUser
from django.contrib.auth import get_user_model
User = get_user_model()


@receiver(post_save,sender=User)
def send_activation_email(sender,instance,created,**kwargs):
    if created:
        token = default_token_generator.make_token(instance)
        
        activation_url = f"{settings.FRONTEND_URL}/users/activate/{instance.id}/{token}/"

        subject = "Activate Your Account"
        message = f"Hi {instance.username},\n\nPlease activate your account by clicking the link below.\n{activation_url}\n\nThank You!"
        recepient_list = [instance.email]
        
        # signals.py
        try:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                recepient_list,
                fail_silently=False,
            )
        except Exception as e:
            print(f"EMAIL ERROR: {type(e).__name__} → {str(e)}")
           




@receiver(post_save,sender=User)
def assign_role(sender, instance,created, **kwargs):
    if created:
        user_group, created =Group.objects.get_or_create(name='User')
        instance.groups.add(user_group)
        instance.save()