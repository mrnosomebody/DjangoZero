from django.urls import path
import maker.views as maker_views

urlpatterns = [
    path('', maker_views.index)
]
