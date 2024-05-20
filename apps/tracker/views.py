from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tracker.models import Transaction
from django.http import HttpRequest
from django.views import View
from django.utils.decorators import method_decorator
from tracker.filters import TransactionFilter

# Create your views here.
class IndexView(View):
    def get(self, request: HttpRequest):
        return render(request, 'index.html')


@method_decorator([login_required], name='dispatch')
class ListTransactionsView(View):
    def get(self, request: HttpRequest):
        transaction_filter = TransactionFilter(
            request.GET,
            queryset=Transaction.objects.filter(
                user=request.user
            ).select_related('category'),
        )
        total_income = transaction_filter.qs.get_total_income()
        total_expenses = transaction_filter.qs.get_total_expenses()

        context = {
            'filter': transaction_filter,
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_income': total_income - total_expenses,
        }

        if request.htmx:
            return render(
                request, 'partials/transactions-container.html', context
            )

        return render(request, 'transactions-list.html', context)
