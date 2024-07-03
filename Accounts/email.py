# from .serializers import PasswordResetSerializer
# from django.core.mail import send_mail




# def get_reset_link(elf,uid,token):
#      # Construct the password reset link
#         return f"http://localhost:3000/api/user/reset/{uid}/{token}"


# def send_reset_email(self,to_email,reset_link):
#          # Send the password reset email
#         subject = "Password Reset"
#         message = f"Click the following link to reset your password:\n{reset_link}"
#         from_email = "test@gmail.com"  # Replace with your email
#         recipient_list = [to_email]
#         # send_mail(subject, message, from_email, recipient_list)