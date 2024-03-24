from base64 import urlsafe_b64decode, urlsafe_b64encode
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.http import HttpResponse


def send_verification_email(request, user_id = None, email_template = None , subject = None, verify_link_type = None):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'User does not exist.')
        return redirect('account-register')
    
    token = default_token_generator.make_token(user)
    uidb64 = urlsafe_b64encode(force_bytes(user.pk))

    print(token, uidb64)
    
    verification_url = reverse(verify_link_type, kwargs={'uidb64': uidb64, 'token': token})
    user_email = user.email
    username = user.username
    print(username)
    verification_link = request.build_absolute_uri(verification_url)
    email_subject = subject
    email_template = email_template
    message = render_to_string(email_template, {'verification_link': verification_link,})
    
    send_mail(email_subject, message, 'koradamahesh2000@gmail.com', [user_email], html_message=message)



# email verification code...

def verify_email(request, uidb64, token):
    print(uidb64)
    try:
        uid = urlsafe_b64decode(uidb64).decode('utf-8')
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
    

def reset_password(request, uidb64, token):
    print(uidb64)
    uid = None
    if request.method == 'POST':
        print(uidb64)
        try:
            uid = urlsafe_b64decode(uidb64).decode('utf-8')
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
                return render(request, 'auth_accounts/email_templates/password_reset_success.html')
            else:
                # If passwords do not match, display an error message
                return render(request, 'auth_accounts/email_templates/password_reset_form.html', {'message': 'Passwords do not match.'})
        else:
            # If UID or token is invalid, display an error message
            return render(request, 'auth_accounts/email_templates/password_reset_error.html', {'message': 'Invalid link.'})
    else:
        # If the request method is not POST, render the reset password form
        return render(request, 'auth_accounts/email_templates/password_reset_form.html', {'uidb64': uidb64, 'token': token})
    
