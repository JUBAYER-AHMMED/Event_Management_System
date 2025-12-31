from django.http import HttpResponse
from django.shortcuts import render,redirect
from users.forms import CustomRegistraionForm,LoginForm, AssignRoleForm,CreateGroupForm
from django.contrib import messages
from django.db.models import Q,Count

from django.contrib.auth import login,authenticate,logout

from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required,permission_required,user_passes_test

from django.db.models import Prefetch
from events.models import Event


# Create your views here.
def is_admin(user):
    # print(user.groups)
    return user.groups.filter(name = 'Admin').exists()


def signup(request):
    registerForm = CustomRegistraionForm()
    loginForm = LoginForm()
    if request.method == 'POST':
        form = CustomRegistraionForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False
            user.save()
            messages.success(request, "A confirmation mail sent.Please Check your email.")
            return redirect('authpage')
        else:
            print('Form is invalid!')
    context = {
        'registerForm': registerForm,
        'loginForm': loginForm
    }
    
    return render(request,'register/authpage.html',context)



def activate_user(request,user_id,token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('authpage')
        else:
            return HttpResponse('Invalid ID or Token')
    except User.DoesNotExist:
        return HttpResponse('User not found!')




def signin(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, 'register/authpage.html', {
        'loginForm': form
    })


@login_required(login_url='no_permission')
def signout(request):
     if request.method == "POST":
        logout(request)
        return redirect('home')




def authpage(request):
    if request.method == "GET":
      registerForm = CustomRegistraionForm()
      loginForm = LoginForm()
    
    context = {
        'registerForm': registerForm,
        'loginForm': loginForm
    }
    
    return render(request,'register/authpage.html',context)



@login_required
@permission_required("auth.add_group", login_url='no_permission')
def admin_dashboard(request):
    users = User.objects.prefetch_related(
        Prefetch('groups', queryset= Group.objects.all(), to_attr='all_groups')
    ).all()
    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0].name
        else:
            user.group_name = 'No Group Assigned'
    context = {
        'users':users
    }
    return render(request,'admin/dashboard.html', context)


@login_required
@permission_required("auth.add_group", login_url='no_permission')
def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = AssignRoleForm()

    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()  #REMOVE OLD ROLE
            user.groups.add(role)
            messages.success(request,f'User {user.username} has been assigned to the {role.name} role')
            return redirect('admin_dashboard')
    context ={
        'form':form,
    }
    return render(request,'admin/assign_role.html',context)


@login_required
@permission_required("auth.add_group", login_url='no_permission')
def create_group(request):
    form = CreateGroupForm()
    if request.method == "POST":
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request,f'Group {group.name} has been created.')
            return redirect('create_group')
    return render(request, 'admin/create_group.html',{'form':form})



@login_required
@permission_required("auth.view_group", login_url='no_permission')
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()

    return render(request,'admin/group_list.html', {'groups':groups})



def is_manager(user):
    return user.groups.filter(Q(name="Organizer")|Q(name="Admin")).exists()

@login_required(login_url='no_permission')
def dashboard(request):
    if is_admin(request.user):
        return redirect('admin_dashboard')
    elif is_manager(request.user):
        return redirect('organizer')
     
    return redirect('home')

def events_with_participants(request):
    events = (
            Event.objects
            .select_related('category')
            .prefetch_related('participants_users')
            .annotate(total_participants=Count('participants_users', distinct=True))
            .order_by('date')
        )
    
    return render(request,'admin/events_with_participants.html',{'events':events})

def delete_participant_from_any_event(request, event_id, participant_id):
    try:
        user = User.objects.get(id=participant_id)
        event = Event.objects.get(id=event_id)
        event.participants_users.remove(user)
        return redirect('events-with-participants')

    except:
        print('error in delete_participant_from_any_event')


