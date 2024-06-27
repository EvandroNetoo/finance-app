from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.views import View


from tracker.filters import TransactionFilter
from tracker.forms import TransactionForm
from tracker.models import Transaction
from django_htmx.http import HttpResponseClientRedirect, retarget


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

        return render(request, 'list-transactions.html', context)


@method_decorator([login_required], name='dispatch')
class CreateTransactionsView(View):
    def get(self, request: HttpRequest):
        context = {'form': TransactionForm()}
        return render(request, 'partials/create-transaction.html', context)

    def post(self, request: HttpRequest):
        form = TransactionForm(request.POST)
        if not form.is_valid():
            response = render(
                request, 'partials/create-transaction.html', {'form': form}
            )
            return retarget(response, '#transaction-block')

        transaction = form.save(commit=False)
        transaction.user = request.user
        transaction.save()
        messages.success(request, 'Transaction was added successfully!')
        return HttpResponseClientRedirect(reverse('list-transactions'))
