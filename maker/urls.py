from django.urls import path, include
import maker.views as maker_views

urlpatterns = [
    path('add/', include([
        path('user/', maker_views.add_user),
        path('company/', maker_views.add_company),
        path('branch/', maker_views.add_branch),
    ])),
    path('get/', include([
        path('users/', maker_views.get_users),
    ])),
    path('', maker_views.test_queryset)
]
