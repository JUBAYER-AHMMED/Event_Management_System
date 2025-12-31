# from django.db.models.signals import post_save, pre_save , post_delete, m2m_changed
# from django.dispatch import receiver
# from django.core.mail import send_mail

# from django.contrib.auth.models import User, Group

# from django.contrib.auth.tokens import default_token_generator
# from django.conf import settings
# from events.models import Participant


# @receiver(post_save,sender=Participant)
# def send_activation_email_to_confirm_participant(sender,instance,created,**kwargs):
#     if created:
#         token = default_token_generator.make_token(instance)
#         print("instance",instance)
#         activation_url = f"{settings.FRONTEND_URL}/events/rsvp-confirm/{instance.id}/{token}/"

#         subject = "Confirm Your RSVP"
#         message = f"Hi {instance.name},\n\nPlease confirm your RSVP by clicking the link below.\n{activation_url}\n\nThank You!"
#         recepient_list = [instance.email]
        
#         try:
#            send_mail(subject,message,settings.EMAIL_HOST_USER,recepient_list)
#         except Exception as e:
#             print(f"Failed to send email to {instance.email}: {str(e)}")
