
from django.shortcuts import render

from deployments.models import Deployment, Profile


def deployments(request):
    deployments = Deployment.objects.all()

    return render(
        request,
        'webui/deployments/deployments.html.j2',
        context={
            'view': 'deployments',
        }
    )
