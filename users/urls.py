from django.urls import path
from users.views import signup,signin,signout,authpage,activate_user,admin_dashboard,AdminDashboard,assign_role,AssignRoleView,create_group,CreateGroupView,group_list,dashboard,events_with_participants,EventsWithParticipantsView,delete_participant_from_any_event,ProfileView,ChangePassword,CustomPasswordResetView,CustomPasswordResetConfirmView,EditProfileView


from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('auth/', authpage, name='authpage'),

    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('activate/<int:user_id>/<str:token>/', activate_user, name='activate'),
    # path('admin/dashboard', admin_dashboard, name='admin_dashboard'),
    path('admin/dashboard', AdminDashboard.as_view(), name='admin_dashboard'),
    # path('admin/<int:user_id>/assign_role/', assign_role, name='assign_role'),
    path('admin/<int:user_id>/assign_role/', AssignRoleView.as_view(), name='assign_role'),
    # path('admin/create_group',create_group,name='create_group'),
    path('admin/create_group',CreateGroupView.as_view(),name='create_group'),
    path('admin/group_list/',group_list,name='group_list'),
    # path('admin/events-with-participants/',events_with_participants,name='events-with-participants'),
    path('admin/events-with-participants/',EventsWithParticipantsView.as_view(),name='events-with-participants'),
    path('admin/delete_participant_from_any_event/<int:event_id>/<int:participant_id>/',delete_participant_from_any_event,name='delete-participant-from-any-event'),

    path('dashboard/',dashboard,name="dashboard"),

    path('profile/',ProfileView.as_view(), name = 'profile'),
    path('password-change/',ChangePassword.as_view(), name='password-change'),
    path('password-change/done/',PasswordChangeDoneView.as_view(template_name = 'accounts/password_change_done.html'), name = 'password_change_done'),
    path('password-reset/',CustomPasswordResetView.as_view(), name = 'password_reset'),
    path('password-reset/confirm/<uidb64>/<token>/',CustomPasswordResetConfirmView.as_view(), name = 'password_reset_confirm'),
    path('edit-profile/',EditProfileView.as_view(), name = 'edit_profile'),

]
