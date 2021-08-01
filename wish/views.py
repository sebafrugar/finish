from django.shortcuts import render, HttpResponse, redirect 
from wish.models import *
from django.db.models import Count
from django.contrib import messages
import bcrypt


# Create your views here.



def main(request):
    return render(request, 'login.html')

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect ('/login')

    else:
        if request.method == 'POST':
            password = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'],password=password,birth_date=request.POST['birth'])
            request.session['id'] = user.id
            print(user.id)
            return redirect('/success')
        else:
            return redirect('/login')

def login(request):
    if request.method == 'POST':
        user = User.objects.filter(email=request.POST["login_email"])
        if len(user) == 1:
            if bcrypt.checkpw(request.POST['login_password'].encode(), user[0].password.encode()):
                request.session['email'] = request.POST["login_email"]
                request.session['id'] = user[0].id
                print(request.session['email'])
                return redirect('/dashboard')
        return redirect("/")


def logout(request):
    request.session.clear()
    return redirect("/")

def success(request):
    if 'id' in request.session:
        user_id=request.session['id']
        user= User.objects.get(id=user_id)
        context={
            'name': f'{user.first_name} {user.last_name}',
        }
        return render(request, 'success.html', context)
    else:
        return redirect("/")

def dashboard(request): 
    if request.session.get('email') == None:
        return redirect('/') 
    user=User.objects.get(id=request.session['id'])
    user_id=request.session.get('id')
    items = item.objects.all()
    context={
        'name' : f'{user.first_name} {user.last_name}',
        'items' : items,
        'add_item':item.objects.exclude(add_item=user_id),
    }    
    return render(request, 'dashboard.html',context=context)

def create_item(request):
    if request.session.get('email') == None:
        return redirect('/')
    if request.method == "POST":
        items = request.POST["item"]
        id = request.session['id']
        user = User.objects.get(id=id)
        create = item.objects.create(item_name=items, created_at=user )
        print(create)
        return redirect("/dashboard")
    return render(request, 'create_item.html')

def view_item(request,id):
    items = item.objects.get(id=id)
    user_id=request.session.get('id')
    user = User.objects.all()
    thisuser=item.objects.get(id=id).add_item.all()
    print(user)
    context={
        'items':items,
        'user' : user,
        'thisuser' : thisuser,
    }
    return render(request, 'view_item.html',context=context)

def delete(request,id):
    items=item.objects.get(id=id)
    items.delete()
    return redirect("/dashboard")

def add_item(request,id):
    user_id=request.session.get('id')
    items=item.objects.get(id=id)
    added = items.add_item.add(user_id)
    print(added)
    return redirect("/dashboard")

def cancelitem(request,id):
    user_id=request.session.get('id')
    items=item.objects.get(id=id)
    items.add_item.remove(user_id)
    return redirect('/dashboard')