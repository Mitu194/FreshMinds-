"""
URL configuration for freshminds project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.models import User,Group
from django.urls import path
from employee import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from employee.views import jobseeker_side  # Ensure this import is correct
from django.urls import path,include
from employee.views import update_overview
from employee.views import user_profile_view
from employee.views import update_overview
from employee.admin import global_admin
from employee.views import delete_education, delete_skill, delete_experience, delete_language, delete_link, delete_summary
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Safely unregister the User model if already registered
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass  # Already unregistered, carry on

# Now register it (custom or default)
admin.site.register(User, UserAdmin)


class CustomLogoutView(LogoutView):
    def get_next_page(self):
        return "/"  # Redirect to custom page

urlpatterns = [

    path('admin/', admin.site.urls),
    path('admin/', global_admin.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # Include authentication URLs
    path('logout/', LogoutView.as_view(next_page=''), name='logout'),
    path('admin/logout/', CustomLogoutView.as_view(), name='admin_logout'),
    path('',views.index),
    path('login',views.login),
    path('signup',views.signup),
    path('job_details',views.job_detail,name='job_details'),
    path('job_details_agency',views.job_details_agency,name='job_details_agency'),
    path('job_details_js',views.job_detail_js),
    path('home',views.home),
    path('home_js',views.home_js),
    path('home_agency/', views.homepage_agency, name='home_agency'),
    path('agency_home',views.agency_home),
    path('job_seeker/', jobseeker_side, name='job_seeker'),
    path('cv',views.cv),
    path('profile',views.new_profile),
    path('company_home',views.business_profile),
    path('agency_profile',views.agency_profile),
    

    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),

    path('company_post',views.company_post),
    path('agency_post',views.agency_post),
    
    path('company_job',views.company_job),
    path('agency_job',views.agency_job),


    path('update-overview/', update_overview, name='update_overview'),
    path('otp',views.otp),
    path('firstpage',views.firstpage, name='first_page'),
    path('accounts',views.accounts),
    path('Job_Post',views.post_job),
    path('Job_post_agency',views.post_job_agency),
    path('post',views.create_post),
    path('post_agency',views.create_post_agency),

    path('interview',views.interview),
    path('interview_agency',views.interview_agency),
    
    path('jobseeker',views.job_seeker_info),
    path('business_info',views.business_info),
    path('agency_info',views.agency_info),
    path('notification',views.notification),
    path('apply',views.apply),
    path('viewcv',views.view_cv),
    path('applied_jobs',views.applied_jobs),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("reset-password/", views.reset_password, name="reset_password"),
    path('company_home_user',views.company_home_user),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('delete-comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('users/<str:username>/', views.user_profile_view, name='user_profile_view'),  # profile view
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),

    path('user/<str:username>/follow/', views.follow_user, name='follow_user'),
    path('user/<str:username>/unfollow/', views.unfollow_user, name='unfollow_user'),
    path('user/<str:username>/followers/', views.followers_list, name='followers_list'),
    path('user/<str:username>/following/', views.following_list, name='following_list'),



    path('emp',views.emp),
    path('show',views.show),
    path('edit/<int:id>', views.edit),  
    path('update/<int:id>', views.update),  
    path('delete/<int:id>', views.destroy),
    
    path('state',views.state),
    path('showstate',views.showstate),
    path('editstate/<int:id>', views.editstate),
    path('updatestate/<int:id>', views.updatestate),  
    path('deletestate/<int:id>', views.destroystate),
    
    path('cmpct',views.cmpct),
    path('showcmpct',views.showcmpct),
    path('editcmpct/<int:id>',views.editcmpct),
    path('updatecmpct/<int:id>',views.updatecmpct),
    path('deletecmpct/<int:id>',views.destroycmpct),
    
    path('login',views.lgn),
    path('showlogin',views.showlogin),
    path('editlogin/<int:id>',views.editlogin),
    path('updatelogin/<int:id>',views.updatelogin),
    path('deletelogin/<int:id>',views.destroylogin),

    path('pstn',views.pstn),
    path('showpstn',views.showpstns),
    path('editpstn/<int:id>',views.editpstns),
    path('updatepstn/<int:id>',views.updatepstns),
    path('deletepstn/<int:id>',views.destroypstns),

    path('city',views.city),
    path('showcity',views.showcity),
    path('editcity/<int:id>',views.editcity),
    path('updatecity/<int:id>',views.updatecity),
    path('deletecity/<int:id>',views.destroycity),


    path('delete-education/<int:edu_id>/', delete_education, name='delete_education'),
    path('delete-skill/<int:skill_id>/', delete_skill, name='delete_skill'),
    path('delete-experience/<int:exp_id>/', delete_experience, name='delete_experience'),
    path('delete-language/<int:lang_id>/', delete_language, name='delete_language'),
    path('delete-link/<int:link_id>/', delete_link, name='delete_link'),
    path('delete-summary/<int:sum_id>/', delete_summary, name='delete_summary'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)