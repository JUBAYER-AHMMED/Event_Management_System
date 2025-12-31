from django.urls import path
from users.views import signup,signin,signout,authpage,activate_user,admin_dashboard,assign_role,create_group,group_list,dashboard,events_with_participants,delete_participant_from_any_event

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('auth/', authpage, name='authpage'),

    path('logout/', signout, name='logout'),
    path('activate/<int:user_id>/<str:token>/', activate_user, name='activate'),
    path('admin/dashboard', admin_dashboard, name='admin_dashboard'),
    path('admin/<int:user_id>/assign_role/', assign_role, name='assign_role'),
    path('admin/create_group',create_group,name='create_group'),
    path('admin/group_list/',group_list,name='group_list'),
    path('admin/events-with-participants/',events_with_participants,name='events-with-participants'),
    path('admin/delete_participant_from_any_event/<int:event_id>/<int:participant_id>/',delete_participant_from_any_event,name='delete-participant-from-any-event'),

    path('dashboard/',dashboard,name="dashboard")

]
