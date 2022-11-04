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
    return HttpResponse(status=405)


def get_users(request):
    if request.method == 'GET':
        data = []
        fields = ('id', 'first_name', 'last_name', 'is_active', 'is_admin', 'date_joined')
        users = User.objects.all()
        for user in users:
            user_data = {key: user.__dict__[key] for key in fields}
            user_data = json.dumps(user_data, default=str)
            data.append(user_data)
        return HttpResponse(data)
    return HttpResponse(status=405)


@csrf_exempt
def add_company(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if not Company.objects.filter(name=data['name']):
            Company.objects.create(**data)
            return HttpResponse(status=201)
        return HttpResponse(status=400)
    return HttpResponse(status=405)


def add_branch(request):
    ...
