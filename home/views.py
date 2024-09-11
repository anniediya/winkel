from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .utils import send_welcome_email
from .models import OTP,Product,Category
from django.utils import timezone
from random import shuffle
import random
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from.forms import ProductForm
# Create your views here.


def registerfn(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        if not (name and phone and email and password and cpassword):
            messages.error(request, 'All fields are required.')
            return redirect('/reg')

        if password != cpassword:
            messages.error(request, 'Passwords do not match.')
            return redirect('/reg')

        if User.objects.filter(username=phone).exists():
            messages.error(request, 'Phone number already taken.')
            return redirect('/reg')

        user = User.objects.create_user(username=phone, password=password, email=email, first_name=name)
        user.save()
        login(request, user)  # Log the user in after registration
        return redirect('/home')

    return render(request, 'register.html', {'cover': 'show'})

def loginfn(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=phone)
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return redirect('/login')

        # Authenticate using the password if no email is registered
        user = authenticate(username=phone, password=password)
        if user:
            login(request, user)
            return redirect('/home')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('/login')
    else:
        return render(request, 'login.html')

def sampfn(request):
    return render(request, 'sample.html')
def samp2fn(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        

    return render(request, 'sample2.html')



def send_otp(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'send_otp.html', {'error': 'User with this email does not exist.'})
        
        otp = OTP.objects.create(user=user)
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp.otp}',
            'from@example.com',
            [user.email],
            fail_silently=False,
        )
        return redirect('send_otp.html', user_id=user.id)
    
    return render(request, 'send_otp.html')

def verify_otp(request, user_id):
    if request.method == "POST":
        otp_input = request.POST.get('otp')
        try:
            user = User.objects.get(id=user_id)
            otp_record = OTP.objects.filter(user=user).order_by('-created_at').first()
            if otp_record and otp_record.otp == otp_input and otp_record.is_valid():
                # OTP is valid; log in the user or perform the next step
                return redirect('/home')
            else:
                return render(request, 'send_otp.html', {'error': 'Invalid or expired OTP.'})
        except User.DoesNotExist:
            return render(request, 'send_otp.html', {'error': 'User not found.'})

    return render(request, 'send_otp.html')


def homefn(request):
    product=Product.objects.all()
    return render(request, 'index.html',{'product':product})


def add_productfn(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/home')
    else:
        form = ProductForm()
    return render(request, 'staff.html', {'form': form})

# not correct
def viewproductfn(request,P_id):
    category=Category.objects.get(P_id)
    product=Product.objects.get(id=category)

def staffn(request):
    return render(request, 'staff.html')
def full(request):
    product=list(Product.objects.all())
    shuffle(product)
    return render(request, 'fullproduct.html',{'product':product})


def add_productfn(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/home')
    else:
        form = ProductForm()
    return render(request, 'staff.html', {'form': form ,'open':'show'})


# def add_categoriesfn(request):
#     if request.method == 'POST':
#         form = CategoryForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('/home')
#     else:
#         form = CategoryForm()
#     return render(request, 'staff.html', {'form': form ,'op':'show'})


def aboutfn(request):
    return render(request, 'about.html')

def logout(request):
    auth.logout(request)
    return redirect('/login')


def edit_productfn(request,p_id):
    if request.method =='POST':
        product = Product.objects.get(id=p_id)
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('/home')
    else:
        product = Product.objects.get(id=p_id)
        form = ProductForm(instance=product)
    return render(request, 'staff.html', {'form': form ,'en':'show'})