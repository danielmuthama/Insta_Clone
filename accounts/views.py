from django.shortcuts import render, redirect
from .forms import RegistrationForm, UserForm
from .models import UserAccount, Followers_Following
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

# account verification
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate, login, logout

from instagram.models import Post

def login_user(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email = email, password = password)

        if user is not None:
            login(request, user)
            messages.success(request, user.email +' logged in successfull!')
            return redirect('home')

    return render(request, 'accounts/login.html')


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username'].lower()
            fullname = form.cleaned_data['fullname'].lower()
            password = form.cleaned_data['password']

            user = UserAccount.objects.create_user(
                email = email,
                username = username,
                fullname = fullname,
                password = password
            )

            message_subject = 'INSTA CLONE ACTIVATION LINK'
            current_site = get_current_site(request)
            message = render_to_string('accounts/verification.html', {
                'user' : user,
                'token' : default_token_generator.make_token(user),
                'domain' : current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk))
            })
            user.is_active=True
            user.save()
            login(request, user)
            receipient_email = email
            send_mail = EmailMessage(message_subject, message ,to=[receipient_email])
            # send_mail.send()
            messages.success(request, 'Account registered successfull!')
            return redirect('home')

        else: 
            print("The form was not submitted!") 
    form = RegistrationForm()
    context = {"form": form}
    return render(request, 'accounts/register.html', context)

def activate_account(request, uid, token):
    try: 
        uid = urlsafe_base64_decode(uid).decode()
        user = UserAccount._default_manager.get(pk = uid)
    except (ValueError, OverflowError, TypeError, UserAccount.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations your account has been activated!')
        return redirect('login')
    
    else:
        messages.error(request, 'Invalid activation link!')
        return redirect('register')


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def profile(request, pk):
    current_user = UserAccount.objects.get(id=pk)
    logged_in_user = request.user.username
    user_followers = len(Followers_Following.objects.filter(user=current_user))
    user_following = len(Followers_Following.objects.filter(follower=current_user))
    user_followers_all = Followers_Following.objects.filter(user = current_user)
    user_followers1 = []

    for i in user_followers_all:
        user_followers_all = i.follower
        user_followers1.append(user_followers_all)

    if current_user in user_followers1:
        follow_button_value = 'unfollow'
    else:
        follow_button_value = 'follow'

    user = UserAccount.objects.get(id=pk)

    posts = user.post_set.all()
    context = {
        'posts': posts, 
        'user': user,
        'user_followers': user_followers,
        'user_following': user_following,
        'follow_button_value': follow_button_value,
        'current_user': current_user,
        }
    return render(request, 'accounts/profile.html', context )

@login_required(login_url='login')
def edit_profile(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)

    context = {'form': form}
    return render(request, 'accounts/edit_profile.html', context)

@login_required(login_url='login')
def follower_count(request):
    if request.method == 'POST':
       value = request.POST.get('value')
       user = request.POST.get('user')
       follower = request.POST.get('follower')
    #    print(value)
       if value == 'follow':
           followers_cnt = Followers_Following.objects.create(follower=follower, user=user)
           followers_cnt.save()
       else:
           followers_cnt = Followers_Following.objects.get(follower=follower, user=user)
           followers_cnt.delete()

       return redirect('/?user=' + user)

