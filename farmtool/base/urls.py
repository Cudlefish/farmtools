from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name="home"),
    path('login',views.login, name="login"),
    path('signup',views.signup, name="signup"),
    path('homepage1',views.homepage1, name="homepage1"),
    path('tool_list', views.tool_list, name="tool_list"),
    path('profile/', views.profile_page, name="profile"),
    path('tool_details',views.tool_detail, name="tool_details"),
    path('add_tool',views.add_tool,name="add_tool"),
    path('tool/<int:tool_id>/checkout/', views.check_out_tool, name='check_out_tool'),
    path('transaction/<int:transaction_id>/checkin/', views.check_in_tool, name='check_in_tool'),
    path('error',views.error, name="error"),
    path('maintenance', views.maintenance_list, name='maintenance_list'),
    path('maintenance/add/<int:tool_id>/', views.add_maintenance, name='add_maintenance'),
    path('maintenance/complete/<int:maintenance_id>/', views.mark_completed, name='mark_completed'),
    path('reminders', views.reminders, name='reminders')

    
    

    
    
]