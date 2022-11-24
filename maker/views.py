import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from maker.models import Company, User, Branch, CompanyCuisine


class CsrfExemptMeta(type):
    """Metaclass for excluding duplicate @csrf_exempt decorator"""

    def __new__(mcs, name, bases, dict):
        new_cls = super().__new__(mcs, name, bases, dict)
        return csrf_exempt(new_cls)


class View(metaclass=CsrfExemptMeta):
    pass


@csrf_exempt
def add_user(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        if not User.objects.filter(email=data['email']):
            if data.get('is_superuser'):
                data.pop('is_superuser')
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


def test_queryset(request):
    a = Company.objects.get(pk=1)
    print(a.companycuisine_set.all())
    print('===========================')
    b = CompanyCuisine.objects.filter(company__name='Supra')
    print(b)
    # print(a)
    # print(a.branches.all())
    # b = a.filter(email__contains='r')
    # print(a)
    return HttpResponse()

'''
0.000) SELECT "maker_companycuisine"."id", "maker_companycuisine"."company_id",
 "maker_companycuisine"."cuisine_id" FROM "maker_companycuisine"
  INNER JOIN "maker_company" ON ("maker_companycuisine"."company_id" = "maker_company"."id")
   WHERE "maker_company"."name" = 'Supra' LIMIT 21; args=('Supra',); alias=default
(0.000) SELECT "maker_company"."id", "maker_company"."name", "maker_company"."description",
 "maker_company"."email", "maker_company"."rating" FROM "maker_company"
  WHERE "maker_company"."id" = 1 LIMIT 21; args=(1,); alias=default
(0.000) SELECT "maker_cuisine"."id", "maker_cuisine"."name" FROM "maker_cuisine"
 WHERE "maker_cuisine"."id" = 1 LIMIT 21; args=(1,); alias=default
(0.000) SELECT "maker_company"."id", "maker_company"."name", "maker_company"."description",
 "maker_company"."email", "maker_company"."rating" FROM "maker_company"
  WHERE "maker_company"."id" = 1 LIMIT 21; args=(1,); alias=default
(0.000) SELECT "maker_cuisine"."id", "maker_cuisine"."name" FROM "maker_cuisine"
 WHERE "maker_cuisine"."id" = 2 LIMIT 21; args=(2,); alias=default
'''