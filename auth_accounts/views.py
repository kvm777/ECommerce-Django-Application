from base64 import urlsafe_b64decode
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import views as auth_views
import requests
import urllib
import json

from django.contrib.auth.models import User
from store.models import Customer

# Create your views here..
def send_verification_email(request, user_id = None, email_template = None , subject = None, verify_link_type = None):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'User does not exist.')
        return redirect('account-register')
    
    token = default_token_generator.make_token(user)
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

    verification_url = reverse(verify_link_type, kwargs={'uidb64': uidb64, 'token': token})
    user_email = user.email
    username = user.username
    verification_link = request.build_absolute_uri(verification_url)
    email_subject = subject
    email_template = email_template
    message = render_to_string(email_template, {'verification_link': verification_link, 'username':username},)
    
    send_mail(email_subject, message, 'koradamahesh2000@gmail.com', [user_email], html_message=message)


# email verification code...

def verify_email(request, uidb64, token):
    print(uidb64)
    try:
        uid = urlsafe_base64_decode(uidb64).decode('utf-8')
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    print(uid)
    print(user)
    print(token)

    if user is not None and default_token_generator.check_token(user, token):
        # Mark email as verified or activate user account
        user.email_verified = True
        user.is_active = True
        user.save()
        return redirect(reverse('store'))
    else:
        return HttpResponse('Email verification failed.')
    

def account_register(request):
    if request.method == 'POST':
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken")
                return redirect(reverse("account-register"))
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already taken")
                return redirect(reverse("account-register"))
            else:
                # Create user but mark it as inactive until email verification
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password1)
                user.is_active = False
                user.save()

                # Create a Customer object associated with the newly created user
                customer = Customer.objects.create(user=user, name=f"{first_name} {last_name}", email=email)
                
                
                user_id = user.pk
                subject = 'Verify your email'
                email_template = 'auth_accounts/email_templates/email_verification.html'
                verify_link_type = "verify_registration_email"
                

                send_verification_email(request, user_id = user_id, subject=subject,email_template = email_template ,verify_link_type = verify_link_type )
                

                messages.success(request, 'Please check your email to activate your account.')
                return redirect(reverse('account-register'))  # Redirect back to the registration page
        else:
            messages.error(request, "Passwords didn't match")
            return redirect(reverse("account-register"))
        
    return render(request, "auth_accounts/register.html", {"page": "register page"})


# AUTHENTICATION_BACKENDS = ['auth_accounts.custom_auth_backends.EmailAuthBackend']
# account login with username and password, if you want use it, remove the abovr in setings and custom_verification in it

# def account_login(request):
#     if request.method == "POST":
#         email = request.POST['email']
#         password = request.POST['password']

#         user = authenticate(request, email=email, password=password)

#         if user != None:
#             login(request, user)
#             return redirect(reverse("store"))
#         else:
#             messages.info(request, "invalid crediantials")
    
#     return render(request, 'auth_accounts/login.html')


# reCAPTCHA server-side validation
def validate_recaptcha(recaptcha_response):
    # The secret key from your Google reCAPTCHA account
    secret_key = settings.GOOGLE_RECAPTCHA_SECRET_KEY  # Get it from your reCAPTCHA admin panel
    # reCAPTCHA endpoint
    verify_url = "https://www.google.com/recaptcha/api/siteverify"
    # Send a POST request to verify the reCAPTCHA response
    data = {
        'secret': secret_key,
        'response': recaptcha_response,
    }
    response = requests.post(verify_url, data=data)
    return response.json()  # This should return a JSON response with a 'success' key


# account login using email and password

def account_login(request):

    if request.method == "POST":
        email_or_username = request.POST.get('email_or_username')
        password = request.POST.get('password')
        

        # Authentication logic
        if email_or_username and password:
            user = authenticate(request, username=email_or_username, password=password)
            if user is None:
                # If authentication with username fails, try with email
                user = authenticate(request, email=email_or_username, password=password)

            if user is not None:
                login(request, user)
                return redirect(reverse("store"))
            else:
                messages.error(request, "Invalid credentials")
        else:
            messages.error(request, "Please provide both email/username and password")

    return render(request, 'auth_accounts/login.html')



def account_logout(request):
    logout(request)
    return redirect(reverse("store"))



def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Display an error message if the email is not found
            messages.info(request, "Email is not found")
            return redirect(reverse("forgot_password"))

        # Generate a password reset token
        # token = default_token_generator.make_token(user)
        
        # Build password reset link
        # uid = urlsafe_base64_encode(force_bytes(user.pk))
        # print(token, uid)
        # reset_link = f"http:localhost:8001/account/reset_password/{uid}/{token}/"
        # reset_link = reverse('reset_password', kwargs={'uid': uid, 'token': token})

        # Send email with password reset link
        # email_subject = 'Password Reset'
        # email_message = render_to_string('auth_accounts/email_templates/password_reset_email.html', {
        #     'reset_link': reset_link,
        # })
        # send_mail(email_subject, email_message, 'koradamahesh2000@gmail.com', [email],  html_message=email_message)


        user_id = user.pk
        email_subject = 'Password Reset'
        email_template = 'auth_accounts/email_templates/password_reset_email.html'
        reset_link = "reset_password"
        

        send_verification_email(request, subject= email_subject, user_id= user_id, email_template= email_template,verify_link_type= reset_link)

        # Display a message to the user indicating that the email has been sent
        return render(request, "auth_accounts/password_reset_mail_sent_done.html",)

    # Render the forgot password form
    return render(request, 'auth_accounts/forgot_password.html')



def reset_password(request, uidb64, token):
    if request.method == 'POST':
        print(uidb64)
        try:
            uid = urlsafe_base64_decode(uidb64).decode('utf-8')
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        print(uid)
        print(user)
        print(token)    
        
        if user is not None and default_token_generator.check_token(user, token):
            # If UID and token are valid, retrieve new password and confirm password from form
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            # Perform password validation
            if new_password == confirm_password:
                # If passwords match, set the new password for the user
                user.set_password(new_password)
                user.save()

                # Redirect to a success page or display a success message
                return render(request, 'auth_accounts/password_reset_success.html')
            else:
                # If passwords do not match, display an error message
                return render(request, 'auth_accounts/password_reset_form.html', {'message': 'Passwords do not match.'})
        else:
            # If UID or token is invalid, display an error message
            return render(request, 'auth_accounts/password_reset_error.html', {'message': 'Invalid link.'})
    else:
        # If the request method is not POST, render the reset password form
        return render(request, 'auth_accounts/password_reset_form.html', {'uidb64': uidb64, 'token': token})



def dummy_check(request):
    return render(request, 'auth_accounts/password_reset_success.html')

