# ARSAFA SOLUTION

A complete business management system built with Django for small and medium businesses. It helps manage daily tasks such as inventory, sales, POS, invoices, customers, employees, lending, repayment reminders, business notes, and barcode scanning — all in one place.

---

## Features

- **Admin Dashboard**: Get a quick overview of sales, inventory, low stock & nearly expiry alerts, and other key business stats in one place
- **Inventory Management**: Add, modify, search, and organize products by category, monitor stock levels, track expiry dates, and check total inventory valuation.
- **Sales & POS**: Handle sales and POS transactions (both paid and unpaid), with access to complete sales history.
- **Invoicing**: Easily create, edit, and track invoices with payment status and due dates.
- **Customer Management**: Keep customer details, purchase history, total sales, and activity records organized. This will help us to implement the loyalty program later on.
- **Employee Management**: Store and manage employee details, roles, and system access.
- **Lending Module**: Manage customer loans, including interest rates, repayment schedules, and due dates.
- **Email Reminders**: Automatically send reminders for overdue invoices and unpaid loans.
- **Notes**: Create, edit, and delete personal notes, accessible from both the navigation bar and dashboard quick links.
- **Barcode Scanner**: Quickly add products to inventory or select them at POS using barcode scanning.
- **Sales & Reporting**: Visualize sales and inventory insights with interactive charts powered by Chart.js (via CDN).
- **Data Management**: Use admin commands to clear/reset data for testing or new deployments.

---

## Detailed Feature Overview

### 1. Admin Dashboard
- **Centralized Overview:** View today’s sales, customer credit balances, low stock alerts, nearly expiring products and navigation bar — all in one place.
- **Quick Navigation:** Access all major modules (Inventory, Sales, POS, Invoices, Customers, Lending, Employees) from dashboard cards.
- **Alerts:** Alert notification will appear for low stock & nearly expiring producs.
- **Data Reset:** Admins can clear all business data (for testing or new deployments) with a single action.

![alt_text](https://github.com/KHANDAKERALIARIYAN/ARSAFA___Solution/blob/ad4dc7a55f519e18de2480e1713794823a189d25/readme-assets/admin-dashboard.png)

### 2. Inventory Management
- **Product Catalog:** Add, edit, and delete products with details like name, category, quantity, unit price, buying price, expiry date, input date, and barcode.
- **Search, Filter, and Sort:** Find products quickly by name, category etc. and sort by price, expiry, or stock level etc.
- **Low Stock Alerts:** Products below a configurable quantity threshold are highlighted and counted, helping prevent stockouts.
- **Expiry Alerts:** Products nearing expiry (within 7 days) are flagged for timely action. They appears in red color for better visibility.

![alt_text](https://github.com/KHANDAKERALIARIYAN/ARSAFA___Solution/blob/739e6b1090248d682cea1182ef302f2fdcdc89f7/readme-assets/inventory.png)

### 3. Sales & POS (Point of Sale)
- **POS Transactions:** Create and manage sales directly at the point of sale, supporting both paid and unpaid transactions.
- **Order Management:** Track all sales and POS orders, including detailed product breakdowns and customer associations.

![alt_text](https://github.com/KHANDAKERALIARIYAN/ARSAFA___Solution/blob/739e6b1090248d682cea1182ef302f2fdcdc89f7/readme-assets/POS.png)

### 4. Invoicing
- **Invoice List & Filtering:** View all invoices (manual and POS-generated), and search by customer or POS number.
- **Create/Edit Invoices:** Generate invoices for customers, set due dates, and update details if needed.
- **POS Integration:** POS transactions automatically generate corresponding invoices for seamless accounting.
- **Payment Tracking:** Mark invoices as paid/due, update statuses, and track due dates to manage cash flow.

![alt_text](https://github.com/KHANDAKERALIARIYAN/ARSAFA___Solution/blob/739e6b1090248d682cea1182ef302f2fdcdc89f7/readme-assets/invoice.png)

### 5. Customer Management
- **Customer Directory:** Add, edit, and delete customer records with contact info, purchase history, and outstanding balances.
- **Purchase & Balance Tracking:** Automatically aggregate all POS sales for each customer and update their outstanding balances.
- **Outstanding Balances:** Instantly see which customers owe money and how much, with automatic updates from unpaid POS transactions.
- **Activity Log:** Track each customer’s last purchase date and total purchases.
- **Data Integrity Tools:** Management commands to check, fix, or clear customer data, ensuring accuracy.

![alt_text](https://github.com/KHANDAKERALIARIYAN/ARSAFA___Solution/blob/739e6b1090248d682cea1182ef302f2fdcdc89f7/readme-assets/customer.png)

### 6. Employee Management
- **Employee Records:** Maintain employee details including name, NID, role, phone, salary, and joining date etc.
- **Admin Integration:** Manage employees through Django Admin with full CRUD support.

![alt_text](https://github.com/KHANDAKERALIARIYAN/ARSAFA___Solution/blob/739e6b1090248d682cea1182ef302f2fdcdc89f7/readme-assets/employee.png)

### 7. Lending Management
- **Lending Dashboard:** Overview of all lending records, including active, repaid, and overdue loans.
- **Add/Edit Lending Records:** Create or update loans for customers, set interest rates, due dates, and add notes.
- **Repayment & Overdue Tracking:** Mark loans as repaid or overdue, and monitor outstanding amounts.
- **Auto-Lending:** Unpaid POS transactions automatically create or update lending records for the customer.
- **Cleanup & Verification:** Management commands to clean up or verify lending records based on unpaid POS bills.

![alt_text](https://github.com/KHANDAKERALIARIYAN/ARSAFA___Solution/blob/739e6b1090248d682cea1182ef302f2fdcdc89f7/readme-assets/lending.png)

### 8. Email Reminders
- **Overdue Notifications:** Send automatic emails for overdue invoices and unpaid loans.

### 9. Notes
- **Create, View, Edit, Delete Notes:** Add personal notes for reminders, ideas, or tasks. Each note has a title, content, and timestamps.
- **Table View:** All notes are displayed in a sortable table with quick action icons for view, edit, and delete.

![alt_text](https://github.com/KHANDAKERALIARIYAN/ARSAFA___Solution/blob/739e6b1090248d682cea1182ef302f2fdcdc89f7/readme-assets/notes.png)

![alt_text](https://github.com/KHANDAKERALIARIYAN/ARSAFA___Solution/blob/739e6b1090248d682cea1182ef302f2fdcdc89f7/readme-assets/view-notes.png)

### 10. Barcode Scanner
- **Quick Product Entry:** Scan barcodes to add new products directly to inventory, reducing manual entry errors.
- **Integration with Inventory & Sales:** Automatically links scanned products with existing inventory records and sales modules.
- **Fast POS Selection:** Select products instantly at the Point of Sale by scanning, making checkout faster and more accurate.

### 11. Sales & Reporting
- **Interactive Charts:** Visualize sales trends, inventory usage, revenue growth, and top-selling products using Chart.js (via CDN).
- **Summary Cards:** Display key metrics such as total sales, pending payments, and stock levels in clear, visual cards.
- **Decision Support:** Helps managers quickly identify performance gaps, best-selling products, and low-stock items.

---

## Folder Structure
```
accounts/      # User authentication, admin dashboard, base templates
inventory/     # Product models, inventory views, forms, and templates
sales/         # Sales and POS models, analytics, and reporting
invoices/      # Invoice and POS management, templates, and APIs
customers/     # Customer models, forms, dashboards, and utilities
lending/       # Lending models, forms, and dashboards
employees/     # Employee management
ARSAFA___SOLUTION/ # Project settings, URLs, WSGI/ASGI
staticfiles/   # Static assets (CSS, JS, images)
manage.py      # Django management script
requirements.txt # Python dependencies
```

## Setup Instructions
1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd ARSAFA___Solution
   ```
2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # Or
   source venv/bin/activate  # On Mac/Linux
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```
5. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```
6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```
7. **Access the app:**
   Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## Tech Stack
- **Frontend:** HTML, CSS, Bootstrap, JavaScript
- **Backend:** Django (Python)
- **Database:** SQLite (default, can be changed)
- **Visualization:** Chart.js (CDN)
- **PDF Generation:** xhtml2pdf

## Contributors
- Khandaker Ali Ariyan
- Nayef Wasit Siddiqui
- Samiun Alim Auntor

## License
MIT 
