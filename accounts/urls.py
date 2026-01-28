from django.urls import path,include
from knox import views as knox_views
from django.contrib.auth import views as auth_views
from .views import database_backup,GroupCreateAPIView,getGroupList,GroupView,user_group_view,getEditLogs,get_edit_log_view,UserCreateAPIView,UserView,getUserList,getEditLogs,getEmailConfigList,CustomUserLoginAPIView,email_template_view,logoutUser,change_password,get_templates,save_template,get_email_config,save_email_config,email_config_view,getEmailTemplateList,EmailTemplateView,user_create_view

urlpatterns = [
    path('', CustomUserLoginAPIView.as_view(), name='login'),
    path('api/', include('accounts.api_urls')),
    path('user/login', CustomUserLoginAPIView.as_view(), name='user-login'),
    path('logout/',logoutUser,name="logout"),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('change_password/', change_password, name='change-password'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name = "accounts/forgot-password.html"), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name = "accounts/password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = "accounts/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name = "accounts/password_reset_complete.html"), name='password_reset_complete'),
    path('templates/get/', get_templates, name='get_templates'),
    path('templates/save/', save_template, name='save_template'),
    path("email-config/", get_email_config, name="get_email_config"),
    path("email-config/save/", save_email_config, name="save_email_config"),
    path('email-configuration/',email_config_view,name='email-configuration'),
    path('configures/',getEmailConfigList,name='configures'),
    path("template-config/", get_email_config, name="template-config"),
    path('template-view/',email_template_view,name='template-view'),
    path('templates/',getEmailTemplateList,name='templates'),
    path('email-template/<int:pk>/',EmailTemplateView.as_view(),name='email-template'),
    path('users/',user_create_view,name='users'),
    path('accounts/user-list/',getUserList,name='user-list'),
    path('user/<int:pk>/',UserView.as_view(),name='user'),
    path('users/create/', UserCreateAPIView.as_view(), name='user-create'),
    path('edit-logs/',get_edit_log_view,name='edit-logs'),
    path('logs/',getEditLogs,name='logs'),
    path('users/',user_create_view,name='users'),
    path('accounts/user-list/',getUserList,name='user-list'),
    path('user/<int:pk>/',UserView.as_view(),name='user'),
    path('users/create/', UserCreateAPIView.as_view(), name='user-create'),
    
    path('user-groups/',user_group_view,name='user-groups'),
    path('accounts/user-groups/',getGroupList,name='user-group-list'),
    path('user-group/<int:pk>/',GroupView.as_view(),name='user-group'),
    path('user-group/create/', GroupCreateAPIView.as_view(), name='user-group-create'),
    # path("send-email/", views.send_email_api, name="send_email_api"),
     path('database-backup/', database_backup, name='database_backup'),
]
