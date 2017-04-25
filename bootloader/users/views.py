from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.shortcuts import redirect

from rest_framework.authtoken.models import Token

from users.models import SSHAuthorizedKey


def user_login(request):
    if request.method == 'POST':
        user = authenticate(
            username=request.POST.get('username'),
            password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            redirect_url = '/'
            if request.GET.get('next') is not None:
                redirect_url = request.GET.get('next')
            return redirect(redirect_url)
        else:
            return render(
                request,
                'webui/users/login.html.j2',
                context={
                    'message': 'Authentication data is invalid',
                    'username': request.POST.get('username'),
                    'password': request.POST.get('password'),
                })
    else:
        return render(request, 'webui/users/login.html.j2')


@login_required
def user_logout(request):
    logout(request)
    return redirect('/')


@login_required
def user_profile(request):
    return render(
        request,
        'webui/users/profile.html.j2',
        context={
            'view': 'user',
            'subview': 'profile',
        })


def user_register(request):
    template = 'webui/users/register.html.j2'

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if not username or not email or not firstname or not lastname \
           or not password or not password2:
            return render(
                request,
                template,
                context={'message': 'All of the fields are required'})

        if password != password2:
            return render(
                request,
                template,
                context={'message': 'Passwords are not the same'})

        user = User.objects.create_user(username, email, password)
        user.first_name = firstname
        user.last_name = lastname
        user.is_active = False
        user.save()

        return redirect('/')
    else:
        return render(request, template)


@login_required
@staff_member_required
def user_events(request):
    users = User.objects.all()
    return render(
        request,
        'webui/users/events.html.j2',
        context={
            'users': users,
            'view': 'users',
        })


@login_required
def user_tokens(request):
    if request.method == 'POST':
        token = Token.objects.filter(user=request.user)
        if token:
            token[0].delete()
        token = Token.objects.create(user=request.user)

        return redirect('/user/tokens.html')
    else:
        tokens = Token.objects.filter(user=request.user)

        return render(
            request,
            'webui/users/tokens.html.j2',
            context={
                'view': 'user',
                'subview': 'apitokens',
                'tokens': tokens
            })


@login_required
def user_ssh_authorized_keys(request):
    return render(
        request,
        'webui/users/ssh_authorized_keys.html.j2',
        context={
            'view': 'user',
            'subview': 'sshkeys',
        })
