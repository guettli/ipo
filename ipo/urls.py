from django.conf.urls import url


from . import views

urlpatterns = [
    url('datetime-now/', views.datetime_now),
]