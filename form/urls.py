from django.urls import path
from . import views

urlpatterns = [
    path("frequency/",  views.frequency, name="form-freq"),
    path("result/",  views.result, name="form-result"),
]
