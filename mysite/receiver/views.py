from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from django.template import loader
from .models import Customer, Transaction

import csv, io
from django.contrib import messages
from django.contrib.auth.decorators import permission_required


def index(request):
    all_transactions_list = [(x, str(x)) for x in Transaction.objects.all()]
    return render(request, 'receiver/index.html', {'all_transactions_list':all_transactions_list})


def tn_detail(request, transaction_id):
    response = "This is transaction number %s." % transaction_id
    response += '\n   ' + str(get_object_or_404(Transaction, id=transaction_id))
    return HttpResponse(response)


def cr_info(request, customer_id):
    return HttpResponse("This customers id is %s. His name is " % customer_id +
                        str(get_object_or_404(Customer, id=customer_id)))


def get_five(request):
    transactions = Transaction.objects.all()
    sums = {}
    for tn in transactions:
        if tn.customer.name not in sums:
            sums[tn.customer.name] = 0
        sums[tn.customer.name] += tn.total_price
    sorted_sums = [(sums[x], x) for x in list(sums)]
    sorted_sums.sort(reverse=True)
    sorted_sums = sorted_sums[:5]
    result = []
    for sum in sorted_sums:
        customer_desc = {"username":sum[1], "spent_money":sum[0], "gems":set()}
        transactoins_set = Customer.objects.get(name=sum[1]).transaction_set.all()
        for deal in list(transactoins_set):
            customer_desc["gems"].add(deal.gem_type)
        result.append(customer_desc)
    for one in range(len(result)):
        new_set = set()
        for other in range(len(result)):
            if one == other:
                continue;
            new_set.update(result[other]["gems"])
        result[one]["gems"].intersection_update(new_set)
    return HttpResponse(result)
    return render(request, "receiver/get_five.html", {"top_five_list":result})


@permission_required('admin.can_add_log_entry')
def transaction_upload(request):
    template = "receiver/transaction_upload.html"
    prompt = {
        'Order': "Order of the csv file should be customer, gem_type, total_price, gem_quantity, deal_time"
    }

    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request, "This is not a csv file")

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for row in csv.reader(io_string):
        if Customer.objects.filter(name=row[0]).count() == 0:
            new_customer = Customer(name=row[0])
            new_customer.save()
        current_customer = Customer.objects.get(name=row[0])
        transaction = Transaction(
            customer=current_customer,
            gem_type=row[1],
            total_price=row[2],
            gem_quantity=row[3],
            deal_time=row[4]
        )
        transaction.save()

    context = {}
    return render(request, template, context)

