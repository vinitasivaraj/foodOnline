from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserForm
from .models import User,UserProfile
from vendor.models import Vendor
from django.contrib import messages,auth
from vendor.forms import VendorForm
from.utils import detectUser,send_verification_email
from django.contrib.auth.decorators import login_required,user_passes_test

from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

# Create your views here.
# Restrict vender accessing customer page 
def check_role_vendor(user):
    if user.role==1:
        return True
    else:
        raise PermissionDenied
    
# Restrict cus accessing ven page 
def check_role_customer(user):
    if user.role==2:
        return True
    else:
        raise PermissionDenied


def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are already logged in ')
        return redirect('myAccount')
    elif request.method=='POST':
        form=UserForm(request.POST)
        if form.is_valid():
            # create user using form 
            # password=form.cleaned_data['password']
            # user=form.save(commit=False)
            # user.role= User.CUSTOMER
            # user.set_password(password)
            # user.save()

            # create user using create user method
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role=User.CUSTOMER
            user.save()
            # Send verification
            mail_subject='Please activate your account'
            email_template='accounts/email/account_verfication_email.html'
            send_verification_email(request,user,mail_subject,email_template)


            messages.success(request," Your account has registed sucessfully ")
            return redirect('registerUser')
        else:
            print(form.errors)
        
    else:
        form = UserForm()
    context={
        'form':form,
    }
    return render(request, 'accounts/registerUser.html',context)


def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are already logged in ')
        return redirect('dashboard')
    elif request.method=='POST':
        form=UserForm(request.POST)
        v_form=VendorForm(request.POST,request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role=User.VENDOR
            user.save()
            vendor=v_form.save(commit=False)
            vendor.user=user
            user_profile=UserProfile.objects.get(user=user)
            vendor.user_profile=user_profile
            vendor.save()


            mail_subject='Please activate your account'
            email_template='accounts/email/account_verification_email.html'
            send_verification_email(request,user,mail_subject,email_template)


            messages.success(request,'Your account has been registed ! Please wait for approval')
            return redirect("registerVendor")
        else:
            print(form.errors)



    else:
        form=UserForm()
        v_form=VendorForm()
    context={
        'form':form,
        'v_form':v_form,
    }
    return render(request,'accounts/registerVendor.html',context)


def activate(request, uidb64, token):
    # Activate the user by setting the is_active status to True
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        # print(user)
        user.is_active = True
        user.save()
        
        messages.success(request, 'Congratulation! Your account is activated.')
        return redirect('myAccount')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('myAccount')




def login(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are already logged in ')
        return redirect('myAccount')
    elif request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        user=auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,"You are logged in")
            return redirect("myAccount")
        else:
            messages.error(request,'Invalid login')
            return redirect("login")


    
    return render(request,'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request,'You have logged out' )
    return redirect('login')

@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)  
    return redirect(redirectUrl) 

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render(request,"accounts/custDashboard.html")
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
   
    return render(request,"accounts/vendorDashboard.html")



def forgot_password(request):
    if request.method=='POST':
        email=request.POST['email']
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email__exact=email)
            # send_password_reset_email from util.py 
            mail_subject='Reset Your Password'
            email_template='accounts/email/reset_password_email.html'
            send_verification_email(request,user,mail_subject,email_template)

            messages.success(request,'Password reset link has been sent to your registered email ')
            return redirect('login')
        else:
            messages.error(request,'Account does not exists')
            return redirect('forgot_password')
    return render(request,'accounts/forgot_password.html')


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        # print("Token is valid and user exists:", user)
        # Token is valid
        request.session['uid'] = uid  # Store UID in session
        # print("Session UID:", request.session['uid'])  
        messages.info(request, 'Please reset your password')
        return redirect('reset_password')
    else:
        # Token is invalid or expired
        messages.error(request, 'This link has been expired!')
        return redirect('myAccount')


def reset_password(request):
    if request.method=='POST':
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']

        if password==confirm_password:
            pk=request.session.get('uid')
            user=User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active=True
            user.save()
            messages.success(request,'Password set successfully')
            return redirect('login')
        else:
            messages.error(request,'Password do not match')
            return redirect('reset_password')
    return render(request,'accounts/reset_password.html')


