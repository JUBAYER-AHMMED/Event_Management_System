from django.urls import path
from events.views import home,create_event,create_category,event_details,organizer,delete_event,update_event,category_list,update_category,delete_category,rsvp,confirm_rsvp
urlpatterns = [
    path('create_event/', create_event,name="create-event"),
    path('create_category/', create_category, name="create-category"),
    path('category_list/', category_list, name="category-list"),
    path('event_details/<int:id>/', event_details, name = "event-details"),
    path('organizer/', organizer, name = "organizer"),
    path('update_event/<int:id>/', update_event, name = "update-event"),
    path('update_category/<int:id>/', update_category, name = "update-category"),
    path('delete_event/<int:id>/', delete_event, name = "delete-event"),
    path('delete_category/<int:id>/', delete_category, name = "delete-category"),
    path('rsvp/<int:event_id>/', rsvp, name = "rsvp"),
    path('rsvp-confirm/<int:participant_id>/<int:event_id>/<str:token>/', confirm_rsvp, name = "confirm-rsvp"),

]