from django.shortcuts import render
from manager.models import Product
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from accounts.models import UserType
from django.core.mail import send_mail
from employee.models import employee_customer
# Create your views here.


@login_required(login_url = '/accounts/login/')
def dashboard(request):
    if request.session['user_type']=='manager':
        salesData=[0]*13
        salesCount = [0] * 13
        sales = employee_customer.objects.all()
        if len(sales)!=0:
            for sal in sales:
                salesData[sal.r_date.month]=int(salesData[sal.r_date.month])+int(sal.product.price)
                print(sal.c_name,sal.product.price,sal.r_date.month,sal.r_date.year)
            print(sales[len(sales)-1].r_date.month)
            salcount = employee_customer.objects.raw("SELECT count(id) as count,id,r_date,product_id FROM `employee_employee_customer` GROUP by month(r_date),year(r_date) ")
            for x in salcount:
                print(x.id,x.count,x.r_date,x.product.price)
                salesCount[x.r_date.month]=x.count
            # for leads
            allLeads = UserType.objects.filter(user_type='customer')
            hotleads = employee_customer.objects.raw("SELECT count(id) as count, id,c_name FROM `employee_employee_customer` GROUP by c_name")
            hot =len(hotleads)
            warm =len(allLeads)-hot
            # for lead in allLeads:
            #     if allLeads.user.username not
            return render(request, 'mandashboard.html',
                          {"data": salesCount[1:sales[len(sales) - 1].r_date.month + 1], "sales": sales,
                           "salesData": salesData[1:sales[len(sales) - 1].r_date.month + 1],"hotlead":hot,"warmlead":warm})
        else:
            return render(request,'mandashboard.html')

    else:
        message="Login in as manager to access this page."
        return render(request,'error.html',{'message':message})

@login_required(login_url = '/accounts/login/')
def display_employees(request):
    if request.session['user_type'] == 'manager':
        e = UserType.objects.filter(user_type="employee")
        employee=set()
        for emp in e:
            u= User.objects.filter(id=emp.user_id)
            employee=set(employee).union(set(u))
        print(employee)
        sales= employee_customer.objects.all()
        return render(request,'viewemp.html',{"employee_list":employee ,"sales_list":sales})
    else:
        message = "Login in as manager to access this page."
        return render(request, 'error.html', {'message': message})

@login_required(login_url = '/accounts/login/')
def display_customers(request):
    if request.session['user_type'] == 'manager':
        c = UserType.objects.filter(user_type="customer")
        sales=employee_customer.objects.all()
        customers = set()
        for cus in c:
            u= User.objects.filter(id=cus.user_id)
            customers=set(customers).union(set(u))
        return render(request, 'viewcust.html', {"customers_list":customers,"sales_list":sales} )
    else:
        message="Login in as manager to access this page."
        return render(request,'error.html',{'message':message})

@login_required(login_url = '/accounts/login/')
def display_products(request):
    if request.session['user_type'] == 'manager':
        p=Product.objects.all()
        return render(request, 'viewprod.html', {"product_list":p} )
    else:
        message="Login in as manager to access this page."
        return render(request,'error.html',{'message':message})

@login_required(login_url = '/accounts/login/')
def register_product(request):
    if request.session['user_type'] == 'manager':
        if request.method=='POST':
            pname=request.POST.get('pname','')
            pprice=request.POST.get('price','')
            pdescription=request.POST.get('description','')
            print(pname,pprice,pdescription)
            p=Product(name=pname,price=pprice,description=pdescription)
            p.save()
            u = User.objects.all()
            # to=[]
            # for us in u:
            #     to.append(us.email)
            # send_mail('New product '+pname, pdescription, 'adchaudhari70@outlook.com', to ,fail_silently=False)
        return render(request, 'productform.html')
    else:
        message="Login in as manager to access this page."
        return render(request,'error.html',{'message':message})


@login_required(login_url = '/accounts/login/')
def sendEmailEmp(request):
    if request.session['user_type'] == 'manager':
        e = UserType.objects.filter(user_type="employee")
        if request.method == 'POST':
            print(request.POST.get("to", ""))
            #for emp in e:
                #send_mail(request.POST.get("subject",""),request.POST.get("body",""),request.user.email, [e.user.email], fail_silently=False)
            return render(request, "composeEmail.html", {"list": e})
        else:
            return render(request,"composeEmail.html",{"list":e})
    else:
        message = "Login in as manager to access this page."
        return render(request, 'error.html', {'message': message})

@login_required(login_url = '/accounts/login/')
def sendEmailCus(request):
    if request.session['user_type'] == 'manager':
        c = UserType.objects.filter(user_type="customer")
        if request.method == 'POST':
            print(request.POST.get("to",""))
            #for cus in c:
                #send_mail(request.POST.get("subject",""),request.POST.get("body",""),request.user.email, [c.user.email], fail_silently=False)
            return render(request, "composeEmail.html", {"list": c,"msg":"email sent"})
        else:
            return render(request,"composeEmail.html",{"list":c})
    else:
        message = "Login in as manager to access this page."
        return render(request, 'error.html', {'message': message})