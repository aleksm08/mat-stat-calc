from django.urls import path
from .views import algoritm

urlpatterns = [
    path('', algoritm, name='algoritm'),
    # path('result/', result, name='result'),

]