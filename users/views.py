from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserRegistrationForm, InputForm, DeleteForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.template import loader
from .models import Class

def home(request):
	return render(request, 'users/home.html', {'isHomeActive':'text-white'})
	
def register(request):
	if request.method == "POST":
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			password=form.cleaned_data['password1']
			messages.success(request, f'Hi {username}, your account has been successfully created.')
			new_user = authenticate(username, password,)
			login(request, new_user)
			return redirect('home')
	else:
		form = UserRegistrationForm()
	context = {
		'form':form,
		'isRegisterActive':'text-white'
	}
	return render(request, 'users/register.html', context)
	
@login_required()
def profile(request):
	return render(request, 'users/profile.html', {'isProfileActive':'text-white'})
	
@login_required()
def records(request):
  classes = request.user.classes.all().values()
  template = loader.get_template('website/records.html')
  context = {
		'courses': Class.objects.values('cid'),
    		'classes': classes,
		'isRecordsActive':'text-white',
		'isClassRecord': len(classes), 
  }
  return HttpResponse(template.render(context, request))

@login_required()
def details(request, cid):
	template = loader.get_template('website/stat.html')
	tot_classes = request.user.classes.all().filter(cid=cid).count()
	att_classes = request.user.classes.all().filter(cid=cid,attendance_status='YES').count()
	percentage = att_classes * 100 /tot_classes
	context = {
		'isStatsActive':'text-white',
		'courses': Class.objects.values('cid'),
    		'classes': Class.objects.filter(cid=cid).values(),
		'cid':cid,
		'tot_classes':tot_classes,
		'att_classes':att_classes,
		'n_att_classes':Class.objects.filter(cid=cid,attendance_status='NO').count(),
		'percentage':percentage
  }
	return HttpResponse(template.render(context, request))


@login_required()
def input(request):
  template = loader.get_template('website/inputForm.html')
  if request.method == 'POST':
    form = InputForm(request.POST)
    if form.is_valid():
        date=form.cleaned_data['Date']
        cid=form.cleaned_data['CID']
        code=form.cleaned_data['Code']
        attendance_status=form.cleaned_data['Attended']
        member = Class(user=request.user,date=date,cid=cid,code=code,attendance_status=attendance_status)
        duplicate = Class.objects.filter(user=request.user,date=date, cid=cid, code=code).count()
        if duplicate == 0:
              member.save()
        return redirect ('/input-form')
      
  form = InputForm()
  context = {
		'form':form,
		'isInputActive':'text-white'
	}
  return HttpResponse(template.render(context, request))
  
  
@login_required()
def deleteData(request):
  template = loader.get_template('website/delete.html')
  if request.method == 'POST':
    form = DeleteForm(request.POST)
    if form.is_valid():
        userName=form.cleaned_data['userName']
        if userName == request.user.username:
              member = request.user.classes.all()
              member.delete()
        return redirect ('home')
      
  form = DeleteForm()
  context = {
		'form':form,
	}
  return HttpResponse(template.render(context, request))
