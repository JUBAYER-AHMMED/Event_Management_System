from django.http import HttpResponse
from django.shortcuts import render,redirect
from users.forms import CustomRegistraionForm,LoginForm, AssignRoleForm,CreateGroupForm,CustomPasswordChangeForm,CustomPasswordResetForm,CustomPasswordResetConfirmForm,EditProfileForm
from django.contrib import messages
from django.db.models import Q,Count

from django.contrib.auth import login,authenticate,logout

# from django.contrib.auth.models import User, Group
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required,permission_required,user_passes_test

from django.db.models import Prefetch
from events.models import Event

from django.utils.decorators import method_decorator

#ccbv:
from django.contrib.auth.views import LoginView,PasswordChangeView, PasswordResetView,PasswordResetConfirmView
from django.views.generic import TemplateView,UpdateView, ListView,DetailView,DeleteView

from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import FormView
from django.views.generic import CreateView

from django.shortcuts import get_object_or_404


from django.contrib.auth import get_user_model
User = get_user_model()


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
            user = form.save(commit = False)
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
    
    return render(request,'registration/authpage.html',context)



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

    return render(request, 'registration/authpage.html', {
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
    
    return render(request,'registration/authpage.html',context)



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

@method_decorator(user_passes_test(is_admin, login_url="no_permission"), name="dispatch")
class AdminDashboard(ListView):
    model = User
    template_name = 'admin/dashboard.html'
    context_object_name = 'users'
    def get_queryset(self):
        queryset = User.objects.prefetch_related(
                        Prefetch('groups', queryset= Group.objects.all(), to_attr='all_groups')
                    ).all()
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for user in context['users']:
            if user.all_groups:
                user.group_name = user.all_groups[0].name
            else:
                user.group_name = 'No Group Assigned'
        return context


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

class AssignRoleView(FormView):
    template_name = 'admin/assign_role.html'
    form_class = AssignRoleForm
    success_url = reverse_lazy('admin_dashboard')
    pk_url_kwarg = 'user_id'

    def dispatch(self, request, *args, **kwargs):
        self.user_obj = get_object_or_404(User, id=kwargs.get(self.pk_url_kwarg))
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        role = form.cleaned_data["role"]

        self.user_obj.groups.clear()
        self.user_obj.groups.add(role)

        messages.success(
            self.request,
            f"User {self.user_obj.username} has been assigned to the {role.name} role"
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.user_obj
        return context
    
    def get_initial(self):
        initial = super().get_initial()
        current_group = self.user_obj.groups.first()
        if current_group:
            initial["role"] = current_group
        return initial

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

@method_decorator(user_passes_test(is_admin, login_url="no_permission"), name="dispatch")
class CreateGroupView(CreateView):
    model = Group
    form_class = CreateGroupForm
    template_name = 'admin/create_group.html'
    success_url = reverse_lazy("create_group")

    def form_valid(self,form):
        response = super().form_valid(form)
        messages.success(self.request, f"Group {self.object.name} has been created.")
        return response

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

@method_decorator(user_passes_test(is_admin, login_url="no_permission"), name="dispatch")
class EventsWithParticipantsView(ListView):
    model = Event
    context_object_name = 'events'
    template_name = 'admin/events_with_participants.html'
    def get_queryset(self):
        queryset = (Event.objects
            .select_related('category')
            .prefetch_related('participants_users')
            .annotate(total_participants=Count('participants_users', distinct=True))
            .order_by('date')
        )
        return queryset


def delete_participant_from_any_event(request, event_id, participant_id):
    try:
        user = User.objects.get(id=participant_id)
        event = Event.objects.get(id=event_id)
        event.participants_users.remove(user)
        return redirect('events-with-participants')

    except:
        print('error in delete_participant_from_any_event')


#profile views
    
class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['username'] = user.username
        context['email'] = user.email
        context['name'] = user.get_full_name()
        context['member_since'] = user.date_joined
        context['last_login'] = user.last_login
        # context['bio'] = user.userprofile.bio
        context['bio'] = user.bio
        # context['profile_image'] = user.userprofile.profile_image
        context['profile_image'] = user.profile_image
        context['phone_no'] = user.phone_no
        return context

class EditProfileView(UpdateView):
    model = User
    form_class=EditProfileForm
    template_name = 'accounts/update_profile.html'
    context_object_name = 'form'
    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.save()
        return redirect('profile')

#password change
    
class ChangePassword(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    form_class = CustomPasswordChangeForm

    

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'registration/reset_password.html'
    html_email_template_name = "registration/reset_email.html"

    success_url = reverse_lazy('signin')

    def form_valid(self,form):
        messages.success(self.request, 'A reset email sent.Please Check Your Email.' )
        return super().form_valid(form)
     
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordResetConfirmForm
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy('signin')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()
        print(context)
        return context


    def form_valid(self,form):
        messages.success(self.request, 'Password has been reset successfully.' )
        return super().form_valid(form)
      