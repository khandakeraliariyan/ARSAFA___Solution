from django.shortcuts import render
from inventory.models import Product
from invoices.models import Invoice, POS
from sales.models import Sale
from customers.models import Customer
from lending.models import Lending
from django.utils import timezone
from django.db.models import Sum, F
from datetime import timedelta

def admin_dashboard(request):
    today = timezone.now().date()

    # Total sales today (paid POS)
    total_sales_today = POS.objects.filter(status='paid', date__date=today).aggregate(total=Sum('total'))['total'] or 0

    # Low stock items using product-specific thresholds
    low_stock_items = Product.objects.filter(quantity__lt=F('low_stock_threshold')).count()

    # Low stock products for alert
    low_stock_products = Product.objects.filter(quantity__lt=F('low_stock_threshold'))

    # Nearly expiring products (expiry within 7 days)
    nearly_expire_products = Product.objects.filter(
        expiry_date__isnull=False,
        expiry_date__lte=today + timedelta(days=7),
        expiry_date__gte=today
    )

    # Pending invoices
    pending_invoices = Invoice.objects.filter(status='unpaid').count()

    # Credit balance (unpaid POS)
    credit_balance = POS.objects.filter(status='unpaid').aggregate(total=Sum('total'))['total'] or 0

    # Recent activities (last 5)
    recent_activities = []

    # Last invoice
    last_invoice = Invoice.objects.order_by('-created_at').first()
    if last_invoice:
        recent_activities.append({
            'type': 'invoice',
            'message': 'New invoice created',
            'detail': last_invoice.customer.name,
            'time': last_invoice.created_at.strftime('%b %d, %H:%M')
        })

    # Last paid invoice
    last_paid = Invoice.objects.filter(status='paid').order_by('-updated_at').first()
    if last_paid:
        recent_activities.append({
            'type': 'payment',
            'message': 'Payment received',
            'detail': last_paid.customer.name,
            'time': last_paid.updated_at.strftime('%b %d, %H:%M')
        })

    # Last product added
    last_product = Product.objects.order_by('-input_date').first()
    if last_product and last_product.input_date:
        recent_activities.append({
            'type': 'stock',
            'message': 'Stock updated',
            'detail': last_product.name,
            'time': last_product.input_date.strftime('%b %d, %Y')
        })

    # Last customer added
    last_customer = Customer.objects.order_by('-created_at').first()
    if last_customer:
        recent_activities.append({
            'type': 'customer',
            'message': 'New customer added',
            'detail': last_customer.name,
            'time': last_customer.created_at.strftime('%b %d, %H:%M')
        })

    summary = {
        'total_sales_today': total_sales_today,
        'low_stock_items': low_stock_items,
        'low_stock_products': low_stock_products,
        'nearly_expire_products': nearly_expire_products,
        'pending_invoices': pending_invoices,
        'credit_balance': credit_balance,
    }

    return render(request, 'accounts/admin_dashboard.html', {
        'summary': summary,
        'recent_activities': recent_activities
    })
