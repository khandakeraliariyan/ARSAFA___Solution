from django.shortcuts import render, get_object_or_404, redirect
from .models import Customer
from .forms import CustomerForm
from django.db.models import Sum, Count, Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from invoices.models import POS, Invoice
from sales.models import Sale
from lending.models import Lending

# Create your views here.

@login_required
def customer_dashboard(request):
    search_query = request.GET.get('search', '')
    customers = Customer.objects.all().order_by('-last_purchase')
    
    # Apply search filter if search query exists
    if search_query:
        customers = customers.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query)
        )
    
    total_customers = customers.count()
    
    # Calculate total sales and outstanding balance for all customers
    total_sales = 0
    outstanding_balance = 0
    
    # Update customer data based on POS bills
    for customer in customers:
        # Get all POS bills for this customer
        all_pos_bills = POS.objects.filter(
            customer_name=customer.name, 
            contact_number=customer.phone
        )
        
        # Get paid POS bills
        paid_pos_bills = all_pos_bills.filter(status='paid')
        
        # Get unpaid POS bills
        unpaid_pos_bills = all_pos_bills.filter(status='unpaid')
        
        # Calculate totals
        total_purchases = all_pos_bills.aggregate(total=Sum('total'))['total'] or 0
        customer_outstanding = unpaid_pos_bills.aggregate(total=Sum('total'))['total'] or 0
        
        # Update customer data
        if (customer.total_purchases != total_purchases or 
            customer.outstanding_balance != customer_outstanding):
            customer.total_purchases = total_purchases
            customer.outstanding_balance = customer_outstanding
            customer.save(update_fields=['total_purchases', 'outstanding_balance'])
        
        # Add to dashboard totals
        total_sales += total_purchases
        outstanding_balance += customer_outstanding
    
    context = {
        'total_customers': total_customers,
        'total_sales': total_sales,
        'outstanding_balance': outstanding_balance,
        'customers': customers,
        'search_query': search_query,
    }
    return render(request, 'customers/customers_dashboard.html', context)

@login_required
def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_dashboard')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customers/customer_form.html', {'form': form})

@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    
    if request.method == 'POST':
        # Check for related invoices first
        related_invoices = Invoice.objects.filter(customer=customer)
        related_sales = Sale.objects.filter(customer=customer)
        related_lendings = Lending.objects.filter(customer=customer)
        
        if related_invoices.exists():
            # Cannot delete customer with invoices
            invoice_count = related_invoices.count()
            messages.error(
                request, 
                f'Cannot delete customer "{customer.name}" because they have {invoice_count} associated invoice(s). '
                f'Please delete the invoices first or contact an administrator.'
            )
            return redirect('customer_dashboard')
        
        try:
            customer.delete()
            messages.success(request, f'Customer "{customer.name}" has been deleted successfully.')
        except Exception as e:
            messages.error(request, f'Error deleting customer: {str(e)}')
        
        return redirect('customer_dashboard')
    
    # For GET request, show confirmation page with related data info
    related_invoices = Invoice.objects.filter(customer=customer)
    related_sales = Sale.objects.filter(customer=customer)
    related_lendings = Lending.objects.filter(customer=customer)
    
    context = {
        'customer': customer,
        'related_invoices': related_invoices,
        'related_sales': related_sales,
        'related_lendings': related_lendings,
        'can_delete': not related_invoices.exists(),
    }
    return render(request, 'customers/customer_confirm_delete.html', context)
