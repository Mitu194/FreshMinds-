from django import forms  
from employee.models import Employee, Organization
from employee.models import State 
from employee.models import CompanyCategory
from employee.models import Positions,City
from employee.models import Member
from employee.models import *
class EmployeeForm(forms.ModelForm):  
    class Meta:  
        model = Employee  
        fields = "__all__"  
class StateForm(forms.ModelForm):
    class Meta:
        model = State
        fields = "__all__"
class CompanyCategoryForm(forms.ModelForm):
    class Meta:
        model = CompanyCategory
        fields = "__all__"
class PositionsForm(forms.ModelForm):
    class Meta:
        model = Positions
        fields = "__all__"
class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = "__all__"
class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['cmpname', 'logo', 'state', 'strstatus', 'login','city','address','strmobileno','website','ccid','cmp_strength']

class AgencyForm(forms.ModelForm):
    class Meta:
        model = Agency
        fields = ['cmpname', 'logo', 'state', 'strstatus', 'login','city','address','strmobileno','website']

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__' 
class MemberEducationForm(forms.ModelForm):
    class Meta:
        model = MemberEducation
        fields = ['passingyear', 'institute', 'grade', 'remark']
        exclude = ['member']  # Exclude member field from form
        labels = {
            'passingyear' : 'Passing year', 
            'institute' : 'Institute name', 
            'grade' : 'Grade', 
            'remark' : 'Remark'
        }

class MemberSkillsForm(forms.ModelForm):
    class Meta:
        model = MemberSkills
        fields = ['skills', 'details']
        exclude = ['member']

class MemberExperienceForm(forms.ModelForm):
    class Meta:
        model = MemberExperience
        fields = ['organizationname', 'worktitle', 'workdetails', 'startdate', 'enddate', 'totalmonthexperience']
        exclude = ['member']
        labels = {
            'organizationname' : 'Company name',
             'worktitle' : 'Title',
             'workdetails' : 'Work Detail' ,
             'startdate' : 'Start date', 
             'enddate' : 'End date' , 
             'totalmonthexperience' : ' Experience in month '
        }
class MemberLanguageForm(forms.ModelForm):
    class Meta:
        model = MemberLanguage
        fields = ['language']
        exclude = ['member']

class MemberLinkForm(forms.ModelForm):
    class Meta:
        model = MemberLink
        fields = ['link_name', 'link_url']
        exclude = ['member']
        labels = {
            'link_name' : 'Link name', 
            'link_url' : 'Link URL'
        }

class SummaryForm(forms.ModelForm):
    class Meta:
        model = Summary
        fields = ['description']
        exclude = ['member']

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ['organization','agency']
        labels = {
            'cmpname': 'Company Name',
            'position': 'Job Position',
            'noofvacancies': 'Number of Vacancies',
            'requiredqualification': 'Required Qualification',
            'requiredexperience': 'Required Experience',
            'jobdescription': 'Job Description',
            'jobtype': 'Job Type',
            'applystartdate': 'Application Start Date',
            'lastdate': 'Last Date to Apply',
            'skillsrequired': 'Required Skills',
        }
class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = '__all__' 

class AgencyForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = '__all__' 

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['login','like_count'] 
        labels ={
            'posttitle' : 'Title',
            'postcontent' : ' Upload image or video ',
            'postdesc' : 'Description'
        }   
        postcontent = forms.ImageField() 
        
class ProfileForm(forms.ModelForm):

    class Meta:
        model = Member
        fields = ['profile']

class OverviewForm(forms.ModelForm):
    class Meta:
        model = Overview
        fields = ['overview']
        exclude = ['organization']

class FollowForm(forms.ModelForm):
    class Meta:
        model = Follow
        fields = '__all__' 