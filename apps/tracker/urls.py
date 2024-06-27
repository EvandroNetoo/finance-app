from django.urls import path
from tracker import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path(
        'transactions/',
        views.ListTransactionsView.as_view(),
        name='list-transactions',
    ),
    path(
        'transactions/create/',
        views.CreateTransactionsView.as_view(),
        name='create-transaction',
    ),
]
