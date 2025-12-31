from django.shortcuts import render, redirect
from django.http import HttpResponse
from events.forms import EventModelForm,CategoryModelForm
from events.models import Event, Category
from datetime import date, timedelta,datetime
from django.utils.timezone import localtime
from django.db.models import Q,Count, Max,Min,Avg
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,permission_required


# Create your views here.

from django.db.models import Count
from django.utils import timezone
from datetime import datetime




def home(request):
    if request.user.is_authenticated:
        events = (
            Event.objects
            .select_related('category')
            .prefetch_related('participants_users')
            .annotate(total_participants=Count('participants_users', distinct=True))
            .order_by('date')
        )
        try:
            rsvp_events = Event.objects.select_related('category').filter(participants_users=request.user)
        except:
            rsvp_events = Event.objects.none()
        
        q = request.GET.get('q')
        if q:
            events = events.filter(
                Q(name__icontains=q) |
                Q(location__icontains=q)
            )

        selected_categories = request.GET.getlist('categories')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if selected_categories:
            events = events.filter(category_id__in=selected_categories)

        if start_date:
            events = events.filter(date__gte=start_date)

        if end_date:
            events = events.filter(date__lte=end_date)

        return render(request, 'all_events.html', {
            'events': events,
            'categories': Category.objects.all(),
            'selected_categories': selected_categories,
            'start_date': start_date,
            'end_date': end_date,
            'q': q,
            'rsvp_events':rsvp_events,
        })
    return render(request, 'home.html')



@login_required
@permission_required("events.add_event", login_url='no_permission')
def organizer(request):
    type = request.GET.get('type', 'today')

    now = timezone.now()

    base_query = (
        Event.objects
        .select_related('category')
        .prefetch_related('participants_users')
        .annotate(total_participants=Count('participants_users', distinct=True))
    )

    if type == 'all':
        events = base_query.all()
    elif type == 'past_events':
        events = base_query.filter(date__lt = now.date())
    elif type == 'upcoming_events':
        events = base_query.filter(date__gt = now.date())
    elif type == 'today':
        events = base_query.filter(date = now.date())

    event_info = type,
    
    counts = Event.objects.aggregate(
        total_events = Count('id', distinct=True),
        total_upcoming_events = Count('id', filter=Q(date__gt=now.date()) , distinct=True),
        total_past_events = Count('id', filter=Q(date__lt=now.date()) ,distinct=True ),
        total_participants = Count('participants_users',distinct=True)
    )

    context = {
        "counts" : counts,
        "events" : events,
        "event_info" : event_info,
    }
    
    return render(request, "organizer/organizer.html", context)



@login_required
@permission_required("events.add_event", login_url='no_permission')
def create_event(request):
    e = 'create'
    event_form = EventModelForm()  #for GET
    if request.method == "POST":
        event_form = EventModelForm(request.POST, request.FILES)
        # print("event hit!")
        if event_form.is_valid():
            # print('hitted again!')
            event = event_form.save()
            messages.success(request, 'Event created successfully!')
            return redirect('create-event')
        else:
            print(event_form.errors)

            
    context = {"event_form": event_form , 'e':e}
    return render(request, "event_form.html", context)



@login_required
@permission_required("events.change_event", login_url='no_permission')
def update_event(request, id):
    e = 'update'
    event = Event.objects.get(id = id)
    event_form = EventModelForm(instance = event)  #for GET
    if request.method == "POST":
        event_form = EventModelForm(request.POST,request.FILES, instance = event)
        if event_form.is_valid():
            event = event_form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('update-event', id)
        else:
            print(event_form.errors)

            
    context = {"event_form": event_form, 'e':e}
    return render(request, "event_form.html", context)


@login_required
@permission_required("events.change_category", login_url='no_permission')
def update_category(request, id):
    e = 'update'
    category = Category.objects.get(id = id)
    category_form = CategoryModelForm(instance = category)  #for GET
    if request.method == "POST":
        category_form = CategoryModelForm(request.POST, instance = category)
        if category_form.is_valid():
            category = category_form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('update-category', id)
        else:
            print(category_form.errors)
            
    context = {"category_form": category_form, 'e':e}
    return render(request, "category_form.html", context)




@login_required
@permission_required("events.add_category", login_url='no_permission')
def create_category(request):
    e = 'create'
    category_form = CategoryModelForm()  #for GET
    if request.method == "POST":
        category_form = CategoryModelForm(request.POST)
        if category_form.is_valid():
            """ For Model Form Data """
            category = category_form.save()
            messages.success(request, 'Category created successfully!')
            return redirect('create-category')

            
    context = {"category_form": category_form,
                "e":e,
               }
    return render(request, "category_form.html", context)





@login_required(login_url='no_permission')
def event_details(request, id):
    event = (
        Event.objects
        .filter(id=id)
        .prefetch_related('participants_users')
        .annotate(total_participants=Count('participants_users', distinct=True))
        .first()
    )

    if not event:
        return redirect('home')

    # participant_form = ParticipantModelForm()
    event_datetime = datetime.combine(event.date, event.time)

    event_datetime = timezone.make_aware(
    event_datetime,
    timezone.get_current_timezone()
    )

    # if request.method == "POST":
        # participant_form = ParticipantModelForm(request.POST)
        # if participant_form.is_valid():
        #    email = participant_form.cleaned_data['email'].lower()
        #    name = participant_form.cleaned_data['name']

        #    participant, created = Participant.objects.get_or_create(
            #    email=email,
            #    defaults={'name': name}
        #    )

        #    if participant.events.filter(id=event.id).exists():
            #   messages.warning(request, 'You are already registered for this event.')
        #    else:
            #   participant.events.add(event)
            #   messages.success(request, 'All set! See you at the event.')

        #    return redirect('event-details', id)


    context = {
        "event": event,
        # "participant_form": participant_form,
        "event_start_iso": event_datetime.isoformat(),
    }

    return render(request, "event_details.html", context)

@login_required(login_url='no_permission')
def rsvp(request, event_id):
    event = Event.objects.get(id=event_id)
    user = request.user


    if event.participants_users.filter(id=user.id).exists():
        messages.info(
            request,
            "You have already confirmed your RSVP for this event."
        )
        return redirect("event-details", id=event.id)

    token = default_token_generator.make_token(user)

    activation_url = (
        f"{settings.FRONTEND_URL}/events/rsvp-confirm/"
        f"{user.id}/{event.id}/{token}/"
    )

    send_mail(
        "Confirm Your RSVP",
        f"Hi {user.username},\n\nConfirm here:\n{activation_url}",
        settings.EMAIL_HOST_USER,
        [user.email],
    )

    messages.success(request, "Confirmation email sent.")
    return redirect("event-details", id=event.id)



def confirm_rsvp(request, participant_id, event_id, token):
    user = User.objects.get(id=participant_id)
    event = Event.objects.get(id=event_id)

    if not default_token_generator.check_token(user, token):
        return HttpResponse("Invalid or expired link.")

    if event.participants_users.filter(id=user.id).exists():
        messages.warning(request, "Already confirmed.")
    else:
        event.participants_users.add(user)
        messages.success(request, "RSVP confirmed!\nAll Set!! See You at the event.")

    return redirect("event-details", id=event.id)



@login_required
@permission_required("events.delete_event", login_url='no_permission')
def delete_event(request, id):
    if request.method == 'POST':
        event = Event.objects.get(id = id)
        event.delete()
        messages.success(request, 'Event deleted successfully!')
    return redirect('organizer')


@login_required
@permission_required("events.view_category", login_url='no_permission')
def category_list(request):
    categories = Category.objects.prefetch_related('events').annotate(total_events=Count('events', distinct=True)).all()
    
    # categories = Category.objects.all()

    return render(request, 'category_list.html', {'categories':categories})



@login_required
@permission_required("events.delete_category", login_url='no_permission')
def delete_category(request, id):
    if request.method == 'POST':
        category = Category.objects.get(id = id)
        category.delete()
        messages.success(request, 'Category deleted successfully!')
    return redirect('category-list')