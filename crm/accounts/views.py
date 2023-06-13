from multiprocessing import context
from multiprocessing.connection import deliver_challenge
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.shortcuts import redirect
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decoraters import *
from django.contrib.auth.models import Group
from django.http import HttpResponse


@login_required(login_url="login")
@admin_only
def home(request):
	orders = Order.objects.all()
	customers = Customer.objects.all()
	totalcustomers = customers.count()
	totalorders = orders.count()
	pending = orders.filter(status="Pending").count()
	delivered = orders.filter(status="Delivered").count()
	
	context = {'orders': orders, 'customers': customers,
	 "totalcustomers": totalcustomers,
	  "totalorders": totalorders, "pending": pending,
	   "delivered": delivered}
	return render(request, 'accounts/dashboard.html', context)

@allowed_users(allowed_roles=['admin'])
@login_required(login_url="login")
def products(request):
	products = Products.objects.all()
	return render(request, 'accounts/products.html', {'products':products})

@allowed_users(allowed_roles=['admin'])
@login_required(login_url="login")
def customer(request, pk_test):
	customer = Customer.objects.get(id=pk_test)
	orders = customer.order_set.all()
	totalorders = orders.count()

	myFilter = OrderFilter(request.GET, queryset=orders)
	orders = myFilter.qs
	context = {"customer":customer, "orders":orders, "totalorders": totalorders, "myFilter": myFilter}
	return render(request, 'accounts/customer.html', context)

# from django.forms import modelform_factory
# from myapp.models import Book
# BookForm = modelform_factory(Book, fields=("author", "title"))
def createCustomer(request):
	form = CreateCustomerForm(request.POST)
	if request.method == "POST":
		if form.is_valid:
			form.save()
	context = {"form": form}
	return render(request, "accounts/createcustomer.html", context)

@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10 )

	customer = Customer.objects.get(id=pk)
	formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
	if request.method == 'POST':
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')

	context = {'form':formset}
	return render(request, "accounts/order.html", context)

@allowed_users(allowed_roles=['admin'])
@login_required(login_url="login")
def updateOrder(request, pk):
	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)
	if request.method == "POST":
		print("Printing POST", request.POST)
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect("/")
	context = {"form": form}
	return render(request, "accounts/order.html", context)

@allowed_users(allowed_roles=['admin'])
@login_required(login_url="login")
def deleteOrder(request, pk):
	item = Order.objects.get(id=pk)
	if request.method == "POST":
		item.delete()
		return redirect("/")
	context = {"item": item}
	return render(request, "accounts/delete.html", context)


@unauthenticated_user
def loginpage(request):

	if request.method == "POST":
		username = request.POST.get("username")
		# print(request.POST)
		password = request.POST.get("password")
		user = authenticate(request, username=username, password=password)
		if user != None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username or Password is incorrect')
			
	context = {}
	return render(request, "accounts/login.html", context)


def logoutuser(request):
	
	print(request.user)
	# print("REQUEST =", type(request))
	# print(request.POST.get("username"))
	logout(request)
	return redirect("login")


@unauthenticated_user
def register(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		form = CreateUserForm()
		if request.method == "POST":
			form = CreateUserForm(request.POST)
			if form.is_valid():
				user = form.save()
				username = form.cleaned_data.get('username')
				group = Group.objects.get(name="customer")
				user.groups.add(group)
				Customer.objects.create(user=user)
				messages.success(request, 'Account was created for ' + username)
				return redirect('login')
		context = {"form": form}
		return render(request, "accounts/register.html", context)
	

@login_required(login_url="login")
@allowed_users(allowed_roles=["customer", "admin"])
def userPage(request):
	orders = request.user.customer.order_set.all()
	totalorders = orders.count()
	pending = orders.filter(status="Pending").count()
	delivered = orders.filter(status="Delivered").count()
	# print(orders[0].status)
	# for i in orders:
	# 	print(i.status)
	context = {"orders": orders, "totalorders": totalorders, "pending": pending, "delivered": delivered}
	return render(request, "accounts/user.html", context)

@login_required(login_url="login")
@allowed_users(allowed_roles=["customer", "admin"])
def accountSetting(request):
	customer = request.user.customer
	
	form = CustomerForm(instance=customer)
	print("request.FILES =", request.FILES)
	if request.method == "POST":
		if form.is_valid:
			form = CustomerForm(request.POST, request.FILES, instance=customer)
			form.save()

	context = {"form": form}
	return render(request, "accounts/account_setting.html", context)
