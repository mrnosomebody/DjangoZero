import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from maker.models import Company, User


@csrf_exempt
def add_user(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        if not User.objects.filter(email=data['email']):
            if data.get('is_superuser'):
                User.objects.create_superuser(**data)
                return HttpResponse(status=201)
            else:
                User.objects.create_user(**data)
                return HttpResponse(status=201)

        return HttpResponse(status=400)
    return HttpResponse()


@csrf_exempt
def add_company(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if not Company.objects.filter(name=data['name']):
            Company.objects.create(**data)
            return HttpResponse(status=201)
        return HttpResponse(status=400)
    return HttpResponse()


def add_branch(request):
    ...
