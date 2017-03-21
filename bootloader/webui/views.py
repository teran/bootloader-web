from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, render_to_response, redirect

from core.models import Location, Server


@login_required
def index(request):
    servers = Server.objects.all()

    return render(
        request,
        'webui/servers/servers.html.j2',
        context={
            'servers': servers,
            'view': 'servers'
        })


@login_required
def locations(request):
    servers = Location.objects.all()

    return render(
        request,
        'webui/servers/locations.html.j2',
        context={
            'locations': locations,
            'view': 'locations'
        })


@login_required
def server(request, pk, fqdn):
    server = get_object_or_404(Server, pk=pk, fqdn=fqdn)

    if request.GET.get('action') == 'edit':
        return render_to_response(
            'webui/servers/server-edit.html.j2',
            context={
                'server': server,
                'view': 'servers',
            })
    else:
        return render(
            request,
            'webui/servers/server.html.j2',
            context={
                'server': server,
                'view': 'servers',
            })


def user_login(request):
    if request.method == "POST":
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(
                request,
                'webui/user/login.html.j2',
                context={
                    'message': 'Authentication data is invalid',
                    'username': request.POST.get('username'),
                    'password': request.POST.get('password'),
                })
    else:
        return render(request,
            'webui/user/login.html.j2')


@login_required
def user_logout(request):
    logout(request)
    return redirect('/')


def user_profile(request):
    return render(request, 'webui/user/profile.html.j2')


def user_register(request):
    template = 'webui/user/register.html.j2'

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if not username or not email or not firstname or not lastname or not password or not password2:
            return render(request, template, context={'message': 'All of the fields are required'})

        if password != password2:
            return render(request, template, context={'message': 'Passwords are not the same'})

        user = User.objects.create_user(username, email, password)
        user.first_name = firstname
        user.last_name = lastname
        user.save()

        return redirect('/')
    else:
        return render(request, template)
