from django.shortcuts import render

def receipt_view(request):
    services = [
        {'name': 'Service A', 'price': 100.00},
        {'name': 'Service B', 'price': 50.00},
        {'name': 'Service C', 'price': 75.00}
    ]
    total_price = 225.00

    context = {
        'services': services,
        'total_price': total_price
    }

    return render(request, 'notajasa.html', context)
