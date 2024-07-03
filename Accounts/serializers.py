# from xml.dom import ValidationErr
from rest_framework.exceptions import ValidationError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import DjangoUnicodeDecodeError, force_bytes, smart_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers

from Accounts.utils import Util
from django.core.mail import send_mail
from django.conf import settings
from .models import User
from .profile import Profile


# def Contact_Validate(value):
#     contact = str(value)
#     if (contact.startswith('98') or contact.startswith('97')) or len(contact) != 10 :
#         raise serializers.ValidationError("the contact number should starts with 98 or 97 and should be of 10 digits.")

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"})
    # contact = serializers.IntegerField(validators = [Contact_Validate])

    class Meta:
        model = User
        # fields = ["name", "email", 'contact',"password", "password2","role",]
        fields = '__all__'
        extra_kwargs = {"password2": {"write_only": True}}

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")
        if password != password2:
            raise serializers.ValidationError(
                "password and confirm passworrd doesnt match"
            )
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ["email", "password"]


# ## making user profile serializer for accessing instance user
class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source = 'user.email',read_only = True)
    
    class Meta:
        model = Profile
        fields = ["id", "email", "name","contact","image"]
        # fields = ['id','email']

# serializeer for User Profile
class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude=('password','is_active','is_admin','role','created_at','updated_at',)


class UserPasswordChangeSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )
    password2 = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )

    class Meta:
        model = User
        fields = ["password", "password2"]

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")
        user = self.context.get("user")
        if password != password2:
            raise serializers.ValidationError(
                "password and conformation password does not match"
            )

        user.set_password(password)
        user.save()
        return attrs


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ["email"]

    def validate(self, attrs):
        email = attrs.get("email")
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            domain=settings.FRONTEND_DOMAIN.rstrip('/')
            reset_link=f'{domain}/{settings.REST_PASSWORD_ENDPOINT}/{uid}/{token}'
            # link = "http://localhost:3000/api/user/reset/" + uid + "/" + token
            #  Construct the reset link
        
            user.save()
            
            uid=urlsafe_base64_encode(force_bytes(user.id)) 
            send_mail(
                "testing",
                "Here is the message.",
                "napaofficial7@gmail.com",
                ["napaofficial7@gmail.com"],
                fail_silently=False,)
            body = f"""
                Click the link to reset your password:

                {reset_link}
            """
            data = {"subject": "EduAid: Reset Password", "body": body, "to_email": user.email}
            Util.send_email(data)
            # Util.send_email(data)
              # Send email with the reset link
          

            return attrs
        else:
            raise serializers.ValidationError("You are not a registered error")
            # raise serializers.ValidationError("you are not a registered error")

        # from django.core.mail import send_mail




    def get_reset_link(elf,uid,token):
        # Construct the password reset link
            return f"http://localhost:3000/api/user/reset/{uid}/{token}"


    # def send_reset_email(self,to_email,reset_link):
    #         # Send the password reset email
    #         subject = "Password Reset"
    #         message = f"Click the following link to reset your password:\n{reset_link}"
    #         from_email = "naparajuli11@gmail.com"  # Replace with your email
    #         recipient_list = [to_email]
    #         send_mail(subject, message, from_email, recipient_list)    








class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )
    password2 = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )

    class Meta:
        model = User
        fields = ["password", "password2"]

    def validate(self, attrs):
        try:
            password = attrs.get("password")
            password2 = attrs.get("password2")
            id = self.context.get("uid")
            token = self.context.get("token")
            print(id)
            if password != password2:
                raise serializers.ValidationError(
                    "password and conformation password does not match"
                )
            id = urlsafe_base64_decode(id)   ##
            user = User.objects.get(id=id)
            if not user:
                raise serializers.ValidationError("User with specified ID does not exist")
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError("Token is not valid or expaired")
            
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError("token is not valid or expaired")


class TeacherUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ["email","id","name"]

