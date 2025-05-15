from django.contrib import admin
from .models import Employee,State,CompanyCategory,Positions,City,Organization,Member,MemberEducation,MemberExperience,MemberSkills,Job,Application,Comments,Message,Post,Likes,MemberLanguage,MemberLink,Summary,Follow
from .models import *
from django.contrib.admin import AdminSite
from django.db.models import Q
from django.apps import apps
from django.template.response import TemplateResponse  
from django.contrib.admin import AdminSite
from django.urls import reverse,path
from django.utils.html import format_html
from employee.models import Employee  # Import your models

class MyAdminSite(AdminSite):
    site_header = "Freshminds Admin"
    site_title = "Freshminds Admin Portal"
    index_template = "admin/base_site.html"
    change_list_template = "admin/change_list.html"  # Use the custom template

class GlobalAdmin(AdminSite):
    site_header = "Custom Admin"

    def search_view(self, request):
        query = request.GET.get("q", "").strip()
        results = []

        if query:
            for model, model_admin in self._registry.items():  # Iterate over registered models
                search_fields = getattr(model_admin, "search_fields", [])
                if search_fields:
                    q_objects = Q()
                    for field in search_fields:
                        q_objects |= Q(**{f"{field}__icontains": query})
                    
                    results.extend(model.objects.filter(q_objects))

        return TemplateResponse(request, "admin/search_results.html", {"results": results, "query": query})

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("search/", self.admin_view(self.search_view), name="admin_search"),
        ]
        return custom_urls + urls  # Add search URL to Django Admin

global_admin = GlobalAdmin(name="global_admin")

class EmployeeAdminModel(admin.ModelAdmin):
    list_display = ['id','ename','eemail','econtact']
    search_fields = ['ename']

class StateAdminModel(admin.ModelAdmin):
    list_display = ['id','sname']

class CompanyCategoryAdminModel(admin.ModelAdmin):
    list_display = ['id','ccname']

class LoginAdminModel(admin.ModelAdmin):
    list_display = ['id','stremail','strmobileno','strpass','strrole','strstatus','dtmcreatedate','dtmupdatedate'] 

class PositionsAdminModel(admin.ModelAdmin):
    list_display = ['id','positionname','companycategory']

class CityAdminModel(admin.ModelAdmin):
    list_display = ['id','cityname','state']

class OrganizationAdminModel(admin.ModelAdmin):
    list_display = ['id','cmpname','address','city','state','strmobileno','website','logo','strstatus','ccid','cmp_strength']

class AgencyAdminModel(admin.ModelAdmin):
    list_display = ['id','cmpname','address','city','state','strmobileno','website','logo','strstatus']

class MemberAdminModel(admin.ModelAdmin):
    list_display = ['id','position','login','firstname','lastname','gender','dateofbirth','address','strmobileno','city','profile']
    search_fields = ['firstname']

class MemberEducationAdminModel(admin.ModelAdmin):
    list_display = ['id','member','passingyear','grade','institute','remark']

class MemberExperienceAdminModel(admin.ModelAdmin): 
    list_display = ['id','member','organizationname','worktitle','workdetails','startdate','enddate','totalmonthexperience']

class MemberSkillsAdminModel(admin.ModelAdmin):
    list_display = ['id','member','skills','details']

class SummaryAdminModel(admin.ModelAdmin):
    list_display = ['id','member','description']

class JobAdminModel(admin.ModelAdmin):
    list_display = ['id','organization','agency','cmpname','position','noofvacancies','requiredqualification','requiredexperience','jobdescription','jobtype','city','applystartdate','lastdate','skillsrequired']
class ApplicationAdminModel(admin.ModelAdmin):
    list_display = ['id','job','member','applydate','status','remarks','attachment'] 
    search_fields = ['status'] 

class CommentsAdminModel(admin.ModelAdmin):
    list_display = ['id','post','login','commentsdate','comments']

class MessageAdminModel(admin.ModelAdmin):
    list_display = ['id','fromlogin','tologin','msg','msgdt']

class PostAdminModel(admin.ModelAdmin):
    list_display = ['id','login','posttitle','postcontent','postdesc','postdttime']

class LikesAdminModel(admin.ModelAdmin):
    list_display = ['id','login','post']

class MemberLanguageAdminModel(admin.ModelAdmin):
    list_display = ['id','member','language']

class MemberLinkAdminModel(admin.ModelAdmin):
    list_display = ['id','member','link_name','link_url']

class FollowAdminModel(admin.ModelAdmin):
    list_display = ['id','follower','following','followed_on']


admin_site = MyAdminSite()

admin.site = admin_site
admin.autodiscover()
admin.site.register(Employee,EmployeeAdminModel)
admin.site.register(State,StateAdminModel)
admin.site.register(CompanyCategory,CompanyCategoryAdminModel)
admin.site.register(Positions,PositionsAdminModel)
admin.site.register(City,CityAdminModel)
admin.site.register(Organization,OrganizationAdminModel)
admin.site.register(Agency,AgencyAdminModel)
admin.site.register(Member,MemberAdminModel)
admin.site.register(MemberEducation,MemberEducationAdminModel)
admin.site.register(MemberSkills,MemberSkillsAdminModel)
admin.site.register(MemberExperience,MemberExperienceAdminModel)
admin.site.register(Summary,SummaryAdminModel)
admin.site.register(Job,JobAdminModel)
admin.site.register(Application,ApplicationAdminModel)
admin.site.register(Comments,CommentsAdminModel)
admin.site.register(Message,MessageAdminModel)
admin.site.register(Post,PostAdminModel)
admin.site.register(Likes,LikesAdminModel)
admin.site.register(MemberLanguage,MemberLanguageAdminModel)
admin.site.register(MemberLink,MemberLinkAdminModel)
admin.site.register(Follow,FollowAdminModel)
