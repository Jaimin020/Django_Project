from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from accounts.forms import SignUpForm
from django.template.context_processors import csrf
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from accounts.models import UserType
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from employee.models import employee_customer
from manager.views import dashboard
from employee.views import totalsale
def home(request):
	return render_to_response('home.html')


# class SignUp(generic.CreateView):
#     form_class = SignUpForm
#     success_url = reverse_lazy('home/')
#     template_name = 'signup.html'

@login_required(login_url = '/accounts/login/')
def changePass(request):
	return render(request,'changePass.html')
@login_required(login_url = '/accounts/login/')
def processChange(request):
	if request.method=='POST':
		id=request.user.id
		user_obj=User.objects.get(id=id)
		old_pass=request.POST.get('old','')
		user = authenticate(username=user_obj.username, password=old_pass)
		if user is not None:
			new_pass = request.POST.get('pwd1', '')
			user_obj.set_password(new_pass)
			user_obj.save()
			#print("NEW PASSWORD"+new_pass)
			#print("OLD PASSWORD"+old_pass)
		return HttpResponseRedirect('/manager/dashboard')


def register (request):
	if request.method=='POST':
		form=SignUpForm(request.POST)
		if form.is_valid():
			user_type = request.POST.get('user_type','')
			user_name = request.POST.get('username', '')
			print(user_type)
			form.save()

			t = User.objects.get(username=user_name)
			u = UserType.objects.get(user_id=t.id)
			u.user_type=user_type
			u.user_name=user_name
			u.save()
			return render_to_response('login.html',{"username":user_name,"password":request.POST.get('password', '')})
		else:
			return render(request,'signup.html',{"msg":form.errors})
	else:
		form = SignUpForm()
	args = {'form': form,"msg":form.errors}
	return render(request, 'signup.html', args)


@login_required(login_url = '/accounts/login/')
def changePass(request):
	return render(request,'changePass.html')
@login_required(login_url = '/accounts/login/')
def processChange(request):
	if request.method=='POST':
		id=request.user.id
		user_obj=User.objects.get(id=id)
		old_pass=request.POST.get('old','')
		user = authenticate(username=user_obj.username, password=old_pass)
		if user is not None:
			new_pass = request.POST.get('pwd1', '')
			user_obj.set_password(new_pass)
			user_obj.save()
			#print("NEW PASSWORD"+new_pass)
			#print("OLD PASSWORD"+old_pass)
		return HttpResponseRedirect('/manager/dashboard')

@login_required(login_url = '/accounts/login/')
def info(request):
	uid=User.objects.get(id=request.user.id)
	return render(request,'accountdetails.html',{"user":uid})


@login_required(login_url = '/accounts/login/')
def delete(request):
	eid = request.POST.get("empid",'')
	print(eid)
	sales=employee_customer.objects.filter(e_id=eid)
	superu=User.objects.filter(id=request.user.id)
	print(superu[0].username)
	for s in sales:
		s.e = superu[0]
		s.save()
	ut=UserType.objects.filter(user_id=eid)
	ut.delete()
	uid = User.objects.filter(id=eid)
	uid[0].delete()
	return dashboard(request)

@login_required(login_url = '/accounts/login/')
def empcontroller(request):
	ac=request.POST.get("action","")
	if ac=="profile":
		return viewProfile(request)
	if ac == "reports":
		return totalsale(request)
	else:
		return render(request,"viewemp.html")


@login_required(login_url = '/accounts/login/')
def viewProfile(request):
	acno=request.POST.get("empid",'')
	uid=User.objects.get(id=acno)
	print(uid)
	return render(request,'viewinfo.html',{"employee":uid})

@login_required(login_url = '/accounts/login/')
def update(request):
	if request.method == 'GET':
		u=User.objects.get(id=request.user.id)
		u.first_name=request.GET.get('first_name','')
		u.last_name = request.GET.get('last_name', '')
		u.email = request.GET.get('email', '')
		u.save()
	return info(request)

@login_required(login_url = '/accounts/login/')
def loggedin(request):
	if request.user.is_authenticated:
		sales=employee_customer.objects.filter(c_name=request.user.username)
		print(request.user.username,sales)
		return render(request,'loggedin.html', {"sales":sales})
	else:
		return HttpResponseRedirect('/acounts/login/')

def invalidlogin(request):
	return render_to_response('invalidlogin.html',{"error":"enter valid username or password"})

def login(request):
	c = {}
	c.update(csrf(request))
	return render_to_response('login.html', c)

def auth_view(request):
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	user = auth.authenticate(username=username, password=password)
	print(user)
	if user is not None:
		auth.login(request,user)
		u = UserType.objects.filter(user_name=username)
		request.session['user_type'] = u[0].user_type
		request.session['basefile'] = u[0].user_type+"base.html"
		if u[0].user_type=='manager':
			return HttpResponseRedirect('/manager/dashboard')
		elif u[0].user_type=='employee':
			request.session["username"]=u[0].user_name
			return HttpResponseRedirect('/employee/dashboard')
		elif u[0].user_type=='customer':
			return loggedin(request)
		else:
			return render_to_response('errorpage.html', {'user': u})
	else:
		return HttpResponseRedirect('/accounts/invalidlogin/')


def logout(request):
	auth.logout(request)
	return render_to_response('home.html')
# Create your views here.
