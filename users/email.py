from django.core.mail import send_mail,EmailMessage
import random
from django.conf import settings
from .models import User,otpmodel


class Util1:

    @staticmethod
    def send_email(email):
        otp = random.randint(1000, 9999)
        messaage = f"your otp is {otp}"
        print(messaage)
        email = EmailMessage(
            subject="your account verification email",
            body=messaage,
            from_email=settings.EMAIL_HOST_USER,
            to=[email]
        )
        try:
            user_object = otpmodel.objects.last()
            print(user_object.email)



            user_object .otp= otp


            user_object .save()
            email.send()
        except Exception as e:
            print(e)



class Util:
  @staticmethod
  def send_email(data):
    email = EmailMessage(
      subject=data['subject'],
      body=data['body'],
      from_email=settings.EMAIL_HOST_USER,
      to=[data['to_email']]
    )
    email.send()

