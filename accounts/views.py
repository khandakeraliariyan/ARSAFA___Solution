from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from inventory.models import Product
from invoices.models import Invoice, POS
from sales.models import Sale
from customers.models import Customer
from lending.models import Lending
from django.utils import timezone
from django.db.models import Sum, F
from datetime import timedelta

def custom_login(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'accounts/login.html')

@login_required
def admin_dashboard(request):
    today = timezone.now().date()
    # Total sales today (paid POS)
    total_sales_today = POS.objects.filter(status='paid', date__date=today).aggregate(total=Sum('total'))['total'] or 0
    # Low stock items using product-specific thresholds
    low_stock_items = Product.objects.filter(quantity__lt=F('low_stock_threshold')).count()
    # Low stock products for alert using product-specific thresholds
    low_stock_products = Product.objects.filter(quantity__lt=F('low_stock_threshold'))
    # Nearly expiring products (expiry within 7 days)
    nearly_expire_products = Product.objects.filter(expiry_date__isnull=False, expiry_date__lte=today + timedelta(days=7), expiry_date__gte=today)
    # Pending invoices
    pending_invoices = Invoice.objects.filter(status='unpaid').count()
    # Credit balance (unpaid POS)
    credit_balance = POS.objects.filter(status='unpaid').aggregate(total=Sum('total'))['total'] or 0
    # Recent activities (last 5)
    recent_activities = []
    # New invoice
    last_invoice = Invoice.objects.order_by('-created_at').first()
    if last_invoice:
        recent_activities.append({'type': 'invoice', 'message': 'New invoice created', 'detail': last_invoice.customer.name, 'time': last_invoice.created_at.strftime('%b %d, %H:%M')})
    # Payment received (last paid invoice)
    last_paid = Invoice.objects.filter(status='paid').order_by('-updated_at').first()
    if last_paid:
        recent_activities.append({'type': 'payment', 'message': 'Payment received', 'detail': last_paid.customer.name, 'time': last_paid.updated_at.strftime('%b %d, %H:%M')})
    # Stock updated (last product)
    last_product = Product.objects.order_by('-input_date').first()
    if last_product and last_product.input_date:
        recent_activities.append({'type': 'stock', 'message': 'Stock updated', 'detail': last_product.name, 'time': last_product.input_date.strftime('%b %d, %Y')})
    # New customer
    last_customer = Customer.objects.order_by('-created_at').first()
    if last_customer:
        recent_activities.append({'type': 'customer', 'message': 'New customer added', 'detail': last_customer.name, 'time': last_customer.created_at.strftime('%b %d, %H:%M')})
    summary = {
        'total_sales_today': total_sales_today,
        'sales_growth': 0,  
        'low_stock_items': low_stock_items,
        'low_stock_products': low_stock_products,
        'nearly_expire_products': nearly_expire_products,
        'low_stock_change': 0, 
        'pending_invoices': pending_invoices,
        'pending_invoices_change': 0, 
        'credit_balance': credit_balance,
        'credit_growth': 0,  
    }
    return render(request, 'accounts/admin_dashboard.html', {'summary': summary, 'recent_activities': recent_activities})

def custom_login_redirect(request):
    return redirect('/admin/login/')

def logout_view(request):
    logout(request)
    return redirect('custom_login')
