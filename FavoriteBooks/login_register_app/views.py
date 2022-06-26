from logging import exception
from django.shortcuts import render,HttpResponse,redirect
from .models import User 
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    return render(request,'register_login.html')

def register(request):
    #check if it post..
    if request.method != 'POST':
        return redirect ('/')
    
    #check if its valid..
    errors = User.objects.validRegister(request.POST)
    if(len(errors)>0):
        for key, value in errors.items():
            messages.error(request, value, 'alert alert-danger')
        return redirect('/')
        
    #gather info from post..
    user_first = request.POST.get('first')
    user_last = request.POST.get('last')
    user_email = request.POST.get('email')
    user_pw = request.POST.get('pw')
    birthday = request.POST.get('birthday')

    #hashing pasword..
    pw_hash = bcrypt.hashpw(user_pw.encode(), bcrypt.gensalt()).decode()
    

    #create new user..
    User.objects.create(first_name=user_first,last_name=user_last,email=user_email,password=pw_hash,birthday=birthday)
    id = User.objects.last().id
    return redirect(f'/saveUser/{id}')

def login(request):
    #checking if the request is post.
    if request.method != 'POST':
        return redirect('/')

    #matching user-inputs with the what stored in db.
    errors = User.objects.validLogin(request.POST)
    if (len(errors)>0):
        for key, value in errors.items():
            messages.error(request, value, 'alert alert-danger')
        return redirect('/')

    #fetching for the id to redirect user to success page.
    id = User.objects.filter(email = request.POST['email'])[0].id

    return redirect(f'/saveUser/{id}')

def saveUser(request,id):
    #keeping user logged in
    request.session['userId'] = id
    return redirect('/success')

def success(request):
    
    try:
        id = request.session['userId']   
    except:
        messages.error(request, "Need to login first", 'alert alert-danger')
        return render(request,'success.html')
    
    user = User.objects.get(id=id)
    context = {
        'user' : user
    }
    return render(request,'success.html',context)

def logout (request,id):
    request.session.pop('userId')
    return redirect('/')