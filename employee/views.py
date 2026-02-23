from django.http import JsonResponse
from django.shortcuts import render, redirect
from employee.forms import EmployeeForm
from employee.models import Employee
from employee.forms import StateForm
from employee.models import State  
from employee.models import CompanyCategory
from employee.forms import CompanyCategoryForm

from employee.models import Member
from django.shortcuts import render, redirect, get_object_or_404

from django.shortcuts import render, redirect
from .models import Member, MemberEducation, MemberSkills, MemberExperience, MemberLanguage, MemberLink, Summary
from .forms import (
    MemberEducationForm, 
    MemberSkillsForm, 
    MemberExperienceForm, 
    MemberLanguageForm, 
    MemberLinkForm,
    SummaryForm,
)

from employee.models import Positions
from employee.models import Job
from employee.forms import PositionsForm
from employee.models import City
from employee.forms import CityForm
from employee.forms import OrganizationForm 
from employee.forms import MemberForm
from employee.models import Post
from employee.models import Organization
from employee.models import *
from employee.forms import *
from django.db.models import Q
from django.contrib.auth import  authenticate
from django.contrib.auth import login as authlogin  
from datetime import date
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.  

from django.shortcuts import get_object_or_404, redirect
from .models import Post, Likes

from django.views.decorators.http import require_POST

@require_POST
def like_post(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=post_id)
        already_liked = Likes.objects.filter(post=post, login=request.user).exists()

        if not already_liked:
            Likes.objects.create(post=post, login=request.user)
            post.like_count += 1
            post.save()
        else:
            Likes.objects.filter(post=post, login=request.user).delete()
            post.like_count -= 1
            post.save()

    return redirect(request.META.get('HTTP_REFERER', '/'))  # or wherever your homepage points



from django.shortcuts import get_object_or_404, redirect
from .models import Comments, Post
from django.contrib.auth.decorators import login_required

@login_required
def add_comment(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        comment_text = request.POST.get('comment')

        print("Raw comment text:", comment_text)  # Debug output
        print("User:", request.user, "Authenticated:", request.user.is_authenticated)

        if comment_text and request.user.is_authenticated:
            new_comment = Comments.objects.create(
                post=post,
                login=request.user,
                comments=comment_text.strip()
            )
            print("New comment created:", new_comment)
    return redirect(request.META.get('HTTP_REFERER', '/'))

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Comments
from django.contrib import messages


@login_required
def delete_comment(request, comment_id):
    print("Trying to delete comment ID:", comment_id)

    comment = get_object_or_404(Comments, id=comment_id)
    print("Comment found:", comment)

    if request.user != comment.login:
        return HttpResponseForbidden("You're not allowed to delete this comment.")

    comment.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comments.objects.filter(post=post).order_by('-commentsdate')  # newest first?

    return render(request, 'homepage_js.html', {
        'post': post,
        'comments': comments,
    })

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Only the owner can delete the post
    if post.login != request.user:
        messages.error(request, "You can't delete someone else’s post bro 😭")
        return redirect(request.META.get('HTTP_REFERER', '/'))  # change to your homepage route

    post.delete()
    messages.success(request, 'Post deleted successfully!')

    return redirect(request.META.get('HTTP_REFERER', '/'))  # or wherever your post list is


from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Follow

@login_required
def follow_user(request, username):
    target_user = get_object_or_404(User, username=username)
    if request.user != target_user:
        Follow.objects.get_or_create(follower=request.user, following=target_user)
    return redirect('user_profile_view', username=target_user.username)

@login_required
def unfollow_user(request, username):
    target_user = get_object_or_404(User, username=username)
    Follow.objects.filter(follower=request.user, following=target_user).delete()
    return redirect('user_profile_view', username=target_user.username)

@login_required
def followers_list(request, username):
    user = get_object_or_404(User, username=username)
    followers = Follow.objects.filter(following=user)
    return render(request, 'followers_list.html', {
        'profile_user': user,
        'followers': followers,
    })

@login_required
def following_list(request, username):
    user = get_object_or_404(User, username=username)
    following = Follow.objects.filter(follower=user)
    return render(request, 'following_list.html', {
        'profile_user': user,
        'following': following,
    })



from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import User, Follow, Organization, Overview, Post, Job, Member, MemberEducation, MemberSkills, MemberExperience, MemberLanguage, MemberLink, Summary, Agency, Comments
from .forms import OverviewForm

def user_profile_view(request, username):
    user = get_object_or_404(User, username=username)

    is_following = False
    if request.user.is_authenticated and request.user != user:
        is_following = Follow.objects.filter(follower=request.user, following=user).exists()

    followers_count = Follow.objects.filter(following=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    followers = Follow.objects.filter(following=user)
    following = Follow.objects.filter(follower=user)

    # Common posts and comments logic
    posts = Post.objects.filter(login=user)  # or whatever logic you're using

    comments_by_post = {
        post.id: Comments.objects.filter(post=post).order_by('-commentsdate')
        for post in posts
    }

    # ---------- ORGANIZATION ----------
    organization = Organization.objects.filter(login=user).first()
    if organization:
        overview = Overview.objects.filter(organization=organization).first()
        overview_form = OverviewForm(instance=overview)
        jobs = Job.objects.filter(organization=organization)

        return render(request, 'company_home_user.html', {
            'profile_user': user,
            'organization': organization,
            'overview': overview,
            'overview_form': overview_form,
            'posts': posts,
            'jobs': jobs,
            'comments_by_post': comments_by_post,
            'is_following': is_following,
            'followers_count': followers_count,
            'following_count': following_count,
            'followers': followers,
            'following': following,
        })

    # ---------- MEMBER ----------
    member = Member.objects.filter(login=user).first()
    if member:
        education = MemberEducation.objects.filter(member=member)
        skills = MemberSkills.objects.filter(member=member)
        experience = MemberExperience.objects.filter(member=member)
        languages = MemberLanguage.objects.filter(member=member)
        links = MemberLink.objects.filter(member=member)
        summary = Summary.objects.filter(member=member)

        return render(request, 'member_profile_user.html', {
            'profile_user': user,
            'member': member,
            'education': education,
            'skills': skills,
            'experience': experience,
            'languages': languages,
            'links': links,
            'summary': summary,
            'posts': posts,
            'comments_by_post': comments_by_post,
            'is_following': is_following,
            'followers_count': followers_count,
            'following_count': following_count,
            'followers': followers,
            'following': following,
        })

    # ---------- AGENCY ----------
    agency = Agency.objects.filter(login=user).first()
    if agency:
        overview = Overview.objects.filter(agency=agency).first()
        overview_form = OverviewForm(instance=overview)
        jobs = Job.objects.filter(agency=agency)
        

        return render(request, 'agency_profile_user.html', {
            'profile_user': user,
            'agency': agency,
            'overview': overview,
            'overview_form': overview_form,
            'posts': posts,
            'jobs': jobs,
            'comments_by_post': comments_by_post,
            'is_following': is_following,
            'followers_count': followers_count,
            'following_count': following_count,
            'followers': followers,
            'following': following,
        })

    # ---------- NO PROFILE CASE ----------
    return render(request, 'user_profile.html', {
        'profile_user': user,
        'message': 'This user does not have a member, organization, or agency profile.',
        'is_following': is_following,
        'followers_count': followers_count,
        'following_count': following_count,
        'followers': followers,
        'following': following,
    })

'''
def user_profile_view(request, username):
    user = get_object_or_404(User, username=username)

    is_following = False
    if request.user.is_authenticated and request.user != user:
        is_following = Follow.objects.filter(follower=request.user, following=user).exists()

    followers_count = Follow.objects.filter(following=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    followers = Follow.objects.filter(following=user)
    following = Follow.objects.filter(follower=user)


    organization = Organization.objects.filter(login=user).first()
    overview = Overview.objects.filter(organization=organization).first()
    overview_form = OverviewForm(instance=overview)
    posts = Post.objects.filter(login=user)
    jobs = Job.objects.filter(organization=organization)
    if organization:
        return render(request, 'company_home_user.html', {
            'profile_user': user,
            'organization': organization,
            'overview':overview,
            'overview_form':overview_form, 
            'posts': posts, # Pass the form to the template
            'jobs':jobs,
            'is_following': is_following,
            'followers_count': followers_count,
            'following_count': following_count,
            'followers': followers,
            'following': following,
        })

    # Try to find if user is a member
    member = Member.objects.filter(login=user).first()
    
    education = MemberEducation.objects.filter(member=member)
    skills = MemberSkills.objects.filter(member=member)
    experience = MemberExperience.objects.filter(member=member)
    languages = MemberLanguage.objects.filter(member=member)
    links = MemberLink.objects.filter(member=member)
    summary = Summary.objects.filter(member=member)
    if member:
        return render(request, 'member_profile_user.html', {
            'profile_user': user,
            'member': member,
            'education': education,
            'skills': skills,  
            'experience': experience,
            'languages': languages,
            'links': links,
            'summary': summary,
            'is_following': is_following,
            'followers_count': followers_count,
            'following_count': following_count,
            'followers': followers,
            'following': following,

        })
    agency = Agency.objects.filter(login=user).first()
    overview = Overview.objects.filter(agency=agency).first()
    overview_form = OverviewForm(instance=overview)
    posts = Post.objects.filter(login=user)
    comments_by_post = {
    post.id: Comments.objects.filter(post=post).order_by('-commentsdate')
    for post in posts
}

    jobs = Job.objects.filter(agency=agency)

    if agency:
        return render(request, 'agency_profile_user.html', {
            'profile_user': user,
            'agency': agency,
            'overview':overview,
            'overview_form':overview_form, 
            'posts': posts, # Pass the form to the template
            'jobs':jobs,
            'is_following': is_following,
            'followers_count': followers_count,
            'following_count': following_count,
            'followers': followers,
            'following': following,
            'comments_by_post': comments_by_post, 

        })
    # If user exists but no profile (edge case)
    return render(request, 'user_profile.html', {
        'profile_user': user,
        'message': 'This user does not have a member or organization profile.',
        'is_following': is_following,
        'followers_count': followers_count,
        'following_count': following_count,
        'followers': followers,
        'following': following,
    })
'''

def job_details_agency(request):
    jobid=0
    if request.GET["jobid"]:
        jobid = request.GET["jobid"]    
    
    job = Job.objects.get(id=jobid)

    user = request.user 
    agency = Agency.objects.filter(login=user).first()
    organization = Organization.objects.filter(login=user).first
    member = Member.objects.filter(login=user).first
    if member:
        return render(request, 'job_details_agency.html', {'job':job,'member':member,'agency':agency,})
            
    return render(request,'job_details_agency.html',{'job':job,'agency':agency,'organization':organization,'member':member})


def index(request):
    data = Member.objects.order_by('?')[:3]
    jobs = Job.objects.order_by('?')[:3]
    colors = ['ibm', 'amazon', 'wipro', 'google','dribble']
    for job in jobs:
        job.color = colors[job.id % 5]  

    return render(request,'index.html',{'members':data,'jobs':jobs,'colors':colors})

def login(request):
    msg = ""
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(username=email, password=password)
        print(user)

        if user is not None:
            authlogin(request, user)

            # Check Member
            if Member.objects.filter(login=user).exists():
                return jobseeker_side(request)

            # Check Organization
            if Organization.objects.filter(login=user).exists():
                return firstpage(request)

            # Check Agency
            if Agency.objects.filter(login=user).exists():
                return redirect('/home_agency')  # Replace with your actual view

            msg = "No Candidate, Organization, or Agency attached to this user"
        else:
            msg = "Invalid login details"

    return render(request, 'login.html', {'msg': msg})

def homepage_agency(request):

    jobs = Job.objects.all()
    cities = City.objects.all()
    print("Received GET parameters:", request.GET)  # Debugging line

    jobs = Job.objects.all()


    selected_location = request.GET.get('location')
    if selected_location and selected_location != "--Select location--":
        print(f"Filtering jobs with location: {selected_location}")
        jobs = jobs.filter(city__id=selected_location)  # Ensure correct field reference

    selected_experience = request.GET.get('experience')

# Filter by Experience
    experience_map = {
        "0 - 3 years": (0, 3),
        "4 - 7 years": (4, 7),
        "8 - 10 years": (8, 10),
        "More than 10 years": (10, 50),
    }

    if selected_experience in experience_map:
        min_exp, max_exp = experience_map[selected_experience]
        jobs = jobs.filter(requiredexperience__range=(min_exp, max_exp))

    selected_jobtype = request.GET.get('jobtype')

    if selected_jobtype and selected_jobtype != "--Select Job type--":
        jobs = jobs.filter(jobtype=selected_jobtype)

    selected_position = request.GET.get('position')

    if selected_position and selected_position != "--Select Position--":
        jobs = jobs.filter(position=selected_position)




    user = request.user 
    agency = Agency.objects.filter(login=user).first()
    cities = City.objects.all()

    
    print("Filtered jobs count:", jobs.count())  # Debugging line
        # Assign colors dynamically
    colors = ['ibm', 'amazon', 'wipro', 'google', 'dribble']
    for job in jobs:
        job.color = colors[job.id % len(colors)]
    
    return render(request,'homepage_agency.html',{'jobs':jobs,'colors':colors,'cities':cities,'agency':agency,'jobs': jobs, 'cities': cities,'selected_location': selected_location,'selected_position': selected_position, 'selected_experience': selected_experience,'selected_jobtype': selected_jobtype,})

def agency_home(request):
    user = request.user  # Get logged-in user

    # Retrieve the Member record linked to the logged-in user
    agency = Agency.objects.filter(login=user).first()
    data = Agency.objects.order_by('?')[:6]
    posts = Post.objects.all()

        # 🔄 Fetch all comments with related post and user
    all_comments = Comments.objects.select_related('post', 'login').all()

    # Group comments by post ID
    comments_by_post = defaultdict(list)
    for c in all_comments:
        comments_by_post[c.post_id].append(c)
    return render(request,'agency_home.html',{'posts':posts,'members':data,'user_id': user.id, 'agency': agency,'comments_by_post': comments_by_post})

def forgot_password(request):
    if request.method == "POST":
        username = request.POST.get("username")
        try:
            user = User.objects.get(username=username)  # Find user by username
            request.session['reset_user_id'] = user.id  # Store user ID in session
            return redirect('reset_password')  # Redirect to password reset form
        except User.DoesNotExist:
            messages.error(request, "User not found")

    return render(request, "forgot_password.html")

def reset_password(request):
    user_id = request.session.get('reset_user_id')
    if not user_id:
        return redirect('forgot_password')  # Redirect if no user in session

    user = User.objects.get(id=user_id)
    
    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password == confirm_password:
            user.set_password(new_password)  # Reset password
            user.save()
            update_session_auth_hash(request, user)  # Keep the user logged in
            messages.success(request, "Password successfully updated")
            return redirect("/login")
        else:
            messages.error(request, "Passwords do not match")

    return render(request, "reset_password.html")

def company_home_user(request):
    user = request.user  
    organization = Organization.objects.filter(login=user).first()
    overview = Overview.objects.filter(organization=organization).first()
    overview_form = OverviewForm(instance=overview)
    posts = Post.objects.filter(login=user).prefetch_related('likes', 'comments')


    posts = Post.objects.filter(login=user)

    # Filter jobs for the user's organization
    jobs = Job.objects.filter(organization=organization)

    return render(request, 'company_home_user.html', {
        'user_id': user.id,
        'organization': organization,
        'overview':overview,
        'overview_form':overview_form, 
        'posts': posts, # Pass the form to the template
        'jobs':jobs,
    })



def signup(request):
    return render(request,'signup.html')

def firstpage(request):
    jobs = Job.objects.all()
    cities = City.objects.all()
    print("Received GET parameters:", request.GET)  # Debugging line

    jobs = Job.objects.all()


    selected_location = request.GET.get('location')
    if selected_location and selected_location != "--Select location--":
        print(f"Filtering jobs with location: {selected_location}")
        jobs = jobs.filter(city__id=selected_location)  # Ensure correct field reference

    selected_experience = request.GET.get('experience')

# Filter by Experience
    experience_map = {
        "0 - 3 years": (0, 3),
        "4 - 7 years": (4, 7),
        "8 - 10 years": (8, 10),
        "More than 10 years": (10, 50),
    }

    if selected_experience in experience_map:
        min_exp, max_exp = experience_map[selected_experience]
        jobs = jobs.filter(requiredexperience__range=(min_exp, max_exp))

    selected_jobtype = request.GET.get('jobtype')

    if selected_jobtype and selected_jobtype != "--Select Job type--":
        jobs = jobs.filter(jobtype=selected_jobtype)

    selected_position = request.GET.get('position')

    if selected_position and selected_position != "--Select Position--":
        jobs = jobs.filter(position=selected_position)



    user = request.user 
    organization = Organization.objects.filter(login=user).first()
    colors = ['ibm', 'amazon', 'wipro', 'google','dribble']
    for job in jobs:
        job.color = colors[job.id % 5]  
    cities = City.objects.all()
    
    return render(request,'firstpage.html',{'colors':colors,'cities':cities,'organization':organization,'jobs':jobs,'colors':colors,'cities':cities,'jobs': jobs, 'cities': cities,'selected_location': selected_location,'selected_position': selected_position, 'selected_experience': selected_experience,'selected_jobtype': selected_jobtype,})

def notification(request):
    return render(request,'notification.html')

def job_detail(request):
    jobid=0
    if request.GET["jobid"]:
        jobid = request.GET["jobid"]    
    
    job = Job.objects.get(id=jobid)

    user = request.user 
    organization = Organization.objects.filter(login=user).first()
    return render(request,'job_detail.html',{'job':job,'organization':organization})



def job_detail_js(request):
    user = request.user
    member = Member.objects.filter(login=user).first()
    jobid=0
    if request.GET["jobid"]:
        jobid = request.GET["jobid"]    
    
    job = Job.objects.get(id=jobid)
    
    
    return render(request,'job_details_js.html',{'job':job,'member':member})


def accounts(request):
    return render(request,'account.html')


def home(request):

    

    user = request.user  # Get logged-in user

    # Retrieve the Member record linked to the logged-in user
    organization = Organization.objects.filter(login=user).first()
    data = Member.objects.order_by('?')[:6]
    posts = Post.objects.all()

    
        # 🔄 Fetch all comments with related post and user
    all_comments = Comments.objects.select_related('post', 'login').all()

    # Group comments by post ID
    comments_by_post = defaultdict(list)
    for c in all_comments:
        comments_by_post[c.post_id].append(c)
    return render(request,'homepage.html',{'posts':posts,'members':data,'user_id': user.id, 'organization': organization,'comments_by_post': comments_by_post})

from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, [])


from django.db.models.functions import Random
from collections import defaultdict
from .models import Comments  # Not "Comment" — your model is plural

def home_js(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user = request.user  
    member = Member.objects.select_related('login').filter(login=user).first()
    members = Member.objects.order_by('?')[:6]

    posts = Post.objects.all()
    # 🔄 Fetch all comments with related post and user
    all_comments = Comments.objects.select_related('post', 'login').all()

    # Group comments by post ID
    comments_by_post = defaultdict(list)
    for c in all_comments:
        comments_by_post[c.post_id].append(c)
    

    return render(request, 'homepage_js.html', {
        'posts': posts,
        'user_id': user.id,
        'member': member,
        'members': members,
        'comments_by_post': comments_by_post,
    })


def post_job(request):
    user = request.user
    organization = Organization.objects.filter(login=user).first()
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            org = Organization.objects.filter(login = request.user).get()
            job = form.save(commit=False)  # Don't save yet
            job.organization = org  # Assign the logged-in user's organization
            job.save()  # Now save
            return redirect('/firstpage')  # Redirect to job listing page
        else:
            print(form.errors)  # Debugging: Print form errors in the console

    else:
        form = JobForm()

    return render(request, 'Post_job.html', {'form': form,'organization':organization})

def post_job_agency(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            agency = Agency.objects.filter(login=request.user).first()
            if agency:
                job = form.save(commit=False)
                job.agency = agency
                job.save()
                return redirect('/home_agency')
            else:
                # Handle the case where the agency isn't found
                return render(request, 'Post_Job_agency.html', {
                    'form': form,
                    'agency': None,
                    'error': "Your account is not linked to any agency. Please contact support."
                })
        else:
            print(form.errors)

    else:
        form = JobForm()

    agency = Agency.objects.filter(login=request.user).first()
    return render(request, 'Post_Job _agency.html', {'form': form, 'agency': agency})



def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)  # ✅ Include request.FILES
        if form.is_valid():
            print("hi")  # Debugging message
            post = form.save(commit=False)  # Don't save yet
            
            # ✅ Assign the logged-in user before saving
            post.login = request.user  
            
            post.save()  # Now save
            return redirect('/post')  # Redirect to the post page
        else:
            print(form.errors)  # Debugging: Print form errors in console

    else:
        form = PostForm()
    posts = Post.objects.filter(login=request.user) 

    # 🔄 Fetch all comments with related post and user
    all_comments = Comments.objects.select_related('post', 'login').all()

    # Group comments by post ID
    comments_by_post = defaultdict(list)
    for c in all_comments:
        comments_by_post[c.post_id].append(c)

    return render(request, 'create_post.html', {'form': form, 'posts': posts,'comments_by_post': comments_by_post})

def post_job2(request):
    return render(request,'post_job2.html')

def create_post_agency(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)  # ✅ Include request.FILES
        if form.is_valid():
            print("hi")  # Debugging message
            post = form.save(commit=False)  # Don't save yet
            
            # ✅ Assign the logged-in user before saving
            post.login = request.user  
            
            post.save()  # Now save
            return redirect('/post')  # Redirect to the post page
        else:
            print(form.errors)  # Debugging: Print form errors in console

    else:
        form = PostForm()
    posts = Post.objects.filter(login=request.user) 
    return render(request, 'create_post_agency.html', {'form': form,   'posts': posts})



def interview(request):
    user = request.user
    company = Organization.objects.filter(login=user).first()
    
    if request.POST:
        application = Application.objects.get(id= request.POST.get('applicationid'))
        
        status = request.POST.get("status")
        application.status = status
        application.save()
   
    
    applications = Application.objects.filter(Q(job__organization=company) & Q(status=''))
    shortlistapplications = Application.objects.filter(Q(job__organization=company) & Q(status='ShortList'))
    rejectedapplications = Application.objects.filter(Q(job__organization=company) & Q(status='Reject'))
   


    return render(request,'interview.html',{'company':company,'applications':applications,'shortlistapplications':shortlistapplications,'rejectedapplications':rejectedapplications})

def interview_agency(request):
    user = request.user 
    agency = Agency.objects.filter(login=user).first() 
    company = Agency.objects.filter(login= request.user).get()
    if request.POST:
        application = Application.objects.get(id= request.POST.get('applicationid'))
        status = request.POST.get("status")
        application.status = status
        application.save()
   

    applications = Application.objects.filter(Q(job__agency=company) & Q(status=''))
    
   
    return render(request,'interview_agency.html',{'applications':applications,'agency':agency})        

def job_seeker_info(request):
    print(request.POST)
    positions = Positions.objects.all()
    states = State.objects.all()
    cities = City.objects.all()

    if request.method == "POST":
        print("Received POST Data:", request.POST)  # Debugging
        print("Received FILES Data:", request.FILES)  # Debugging

        password = request.POST.get("strpass")
        confirm_password = request.POST.get("confirmpass")

        if password != confirm_password:
            print("Password mismatch")
            return render(request, 'job_seeker.html', {'error': 'Passwords do not match', 'states': states, 'cities': cities})

        email = request.POST.get("stremail")
        existing_user = User.objects.filter(email=email).first()
        if existing_user:
            print("Email already exists")
            return render(request, 'job_seeker.html', {'error': 'Email already exists', 'states': states, 'cities': cities})

        # Create the user
        try:
            user = User.objects.create_user(username=email, email=email, password=password,first_name=request.POST.get("firstname"),last_name=request.POST.get("lastname"))
            user.save()
            print("User created successfully")
        except Exception as e:
            print("Error creating user:", e)
            return render(request, 'job_seeker.html', {'error': 'User creation failed', 'states': states, 'cities': cities})

        # Create Organization object
        try:
            member = Member()
            member.login = user
            member.firstname = request.POST.get("firstname")
            member.lastname = request.POST.get("lastname")
            member.address = request.POST.get("address")
            member.gender = request.POST.get("gender")
            member.position = request.POST.get("position")
            member.dateofbirth = request.POST.get("dateofbirth")
            # Check if a file was uploaded
            if 'profile' in request.FILES:
                member.profile = request.FILES['profile']
                # organization.logo = request.POST.get("logo")
                print("Profile uploaded successfully")
            else:
                print("No file uploaded.")
   
            member.strmobileno = request.POST.get("strmobileno")
            member.city = City.objects.filter(id=request.POST.get("city")).first()
            member.strstatus = request.POST.get("strstatus")

            member.save()
            print("Member saved successfully")

            return redirect('/login')
        except Exception as e:
            print("Error saving organization:", e)
            return render(request, 'job_seeker.html', {'error': 'Organization creation failed', 'states': states, 'cities': cities})

    return render(request, 'job_seeker.html', {'states': states, 'cities': cities})

def business_info(request):
    print(request.POST)
    categories = CompanyCategory.objects.all()
    states = State.objects.all()
    cities = City.objects.all()

    if request.method == "POST":
        print("Received POST Data:", request.POST)  # Debugging
        print("Received FILES Data:", request.FILES)  # Debugging

        password = request.POST.get("strpass")
        confirm_password = request.POST.get("confirmpass")

        if password != confirm_password:
            print("Password mismatch")
            return render(request, 'business_info.html', {'error': 'Passwords do not match', 'states': states, 'cities': cities, 'categories': categories})

        email = request.POST.get("stremail")
        existing_user = User.objects.filter(email=email).first()
        if existing_user:
            print("Email already exists")
            return render(request, 'business_info.html', {'error': 'Email already exists', 'states': states, 'cities': cities, 'categories': categories})

        # Create the user
        try:
            user = User.objects.create_user(username=email, email=email, password=password,first_name=request.POST.get("cmpname"))
            user.save()
            print("User created successfully")
        except Exception as e:
            print("Error creating user:", e)
            return render(request, 'business_info.html', {'error': 'User creation failed', 'states': states, 'cities': cities, 'categories': categories})

        # Create Organization object
        try:
            organization = Organization()
            organization.login = user
            organization.cmpname = request.POST.get("cmpname")
            organization.address = request.POST.get("address")

            # Check if a file was uploaded
            if 'logo' in request.FILES:
                organization.logo = request.FILES['logo']
                # organization.logo = request.POST.get("logo")
                print("Logo uploaded successfully")
            else:
                print("No file uploaded.")
   
            organization.strmobileno = request.POST.get("strmobileno")
            organization.website = request.POST.get("website")
            organization.state = State.objects.filter(id=request.POST.get("state")).first()
            organization.city = City.objects.filter(id=request.POST.get("city")).first()
            organization.strstatus = request.POST.get("strstatus")
            organization.ccid = CompanyCategory.objects.filter(id=request.POST.get("ccid")).first()
            organization.cmp_strength = request.POST.get("cmp_strength")

            organization.save()
            print("Organization saved successfully")

            return redirect('/login')
        except Exception as e:
            print("Error saving organization:", e)
            return render(request, 'business_info.html', {'error': 'Organization creation failed', 'states': states, 'cities': cities, 'categories': categories})

    return render(request, 'business_info.html', {'states': states, 'cities': cities, 'categories': categories})

def agency_info(request):
    print(request.POST)
    states = State.objects.all()
    cities = City.objects.all()

    if request.method == "POST":
        print("Received POST Data:", request.POST)  # Debugging
        print("Received FILES Data:", request.FILES)  # Debugging

        password = request.POST.get("strpass")
        confirm_password = request.POST.get("confirmpass")

        if password != confirm_password:
            print("Password mismatch")
            return render(request, 'agency_info.html', {'error': 'Passwords do not match', 'states': states, 'cities': cities})

        email = request.POST.get("stremail")
        existing_user = User.objects.filter(email=email).first()
        if existing_user:
            print("Email already exists")
            return render(request, 'agency_info.html', {'error': 'Email already exists', 'states': states, 'cities': cities})

        # Create the user
        try:
            user = User.objects.create_user(username=email, email=email, password=password,first_name=request.POST.get("cmpname"))
            user.save()
            print("User created successfully")
        except Exception as e:
            print("Error creating user:", e)
            return render(request, 'agency_info.html', {'error': 'User creation failed', 'states': states, 'cities': cities})

        # Create Organization object
        try:
            agency = Agency()
            agency.login = user
            agency.cmpname = request.POST.get("cmpname")
            agency.address = request.POST.get("address")

            # Check if a file was uploaded
            if 'logo' in request.FILES:
                agency.logo = request.FILES['logo']
                # organization.logo = request.POST.get("logo")
                print("Logo uploaded successfully")
            else:
                print("No file uploaded.")
   
            agency.strmobileno = request.POST.get("strmobileno")
            agency.website = request.POST.get("website")
            agency.state = State.objects.filter(id=request.POST.get("state")).first()
            agency.city = City.objects.filter(id=request.POST.get("city")).first()
            agency.strstatus = request.POST.get("strstatus")

            agency.save()
            print("Agency saved successfully")

            return redirect('/login')
        except Exception as e:
            print("Error saving Agency:", e)
            return render(request, 'agency_info.html', {'error': 'Agency creation failed', 'states': states, 'cities': cities})

    return render(request, 'agency_info.html', {'states': states, 'cities': cities})

from django.contrib.auth.decorators import login_required


from django.shortcuts import render, get_object_or_404
from .models import Organization
from .forms import OverviewForm  # Ensure you have an OverviewForm

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Organization
from .forms import OverviewForm

def business_profile(request):
    user = request.user  
    organization = Organization.objects.filter(login=user).first()
    overview = Overview.objects.filter(organization=organization).first()
    overview_form = OverviewForm(instance=overview)
    posts = Post.objects.filter(login=request.user)

    posts = Post.objects.filter(login=user)
    latest_post = posts.order_by('-postdttime').first()

    # Filter jobs for the user's organization
    jobs = Job.objects.filter(organization=organization)
    latest_job = jobs.order_by('-posted_date').first()

    return render(request, 'company_home.html', {
        'user_id': user.id,
        'organization': organization,
        'overview':overview,
        'overview_form': overview_form, 
        'posts': posts, # Pass the form to the template
        'jobs':jobs,
        "latest_job": latest_job,
        "latest_post": latest_post,
    })

def agency_profile(request):
    user = request.user  
    agency = Agency.objects.filter(login=user).first()
    overview = Overview.objects.filter(agency=agency).first()
    overview_form = OverviewForm(instance=overview)
    posts = Post.objects.filter(login=request.user)

    posts = Post.objects.filter(login=user)
    latest_post = posts.order_by('-postdttime').first()

    # Filter jobs for the user's organization
    jobs = Job.objects.filter(agency=agency)
    latest_job = jobs.order_by('-posted_date').first()

    return render(request, 'agency_profile.html', {
        'user_id': user.id,
        'agency': agency,
        'overview':overview,
        'overview_form': overview_form, 
        'posts': posts, # Pass the form to the template
        'jobs':jobs,
        "latest_job": latest_job,
        "latest_post": latest_post,
    })


from django.http import JsonResponse
import json
from .models import Organization, Agency, Overview  # adjust imports as needed
@login_required
@csrf_exempt

def update_overview(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    try:
        user = request.user
        data = json.loads(request.body)
        new_text = data.get('overview')

        if not new_text:
            return JsonResponse({'error': 'Overview text is required'}, status=400)

        # Try finding an Organization or Agency tied to the user
        organization = None
        agency = None

        try:
            organization = Organization.objects.get(login=user)
        except Organization.DoesNotExist:
            pass

        try:
            agency = Agency.objects.get(login=user)
        except Agency.DoesNotExist:
            pass

        if not organization and not agency:
            return JsonResponse({'error': 'No organization or agency found for this user'}, status=404)

        # Fetch or create the Overview
        if organization:
            overview, created = Overview.objects.get_or_create(organization=organization)
        else:
            overview, created = Overview.objects.get_or_create(agency=agency)

        # Update and save
        overview.overview = new_text
        overview.save()

        return JsonResponse({'success': True, 'overview': overview.overview})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    except Exception as e:
        import traceback
        print(traceback.format_exc())  # Logs for debugging
        return JsonResponse({'error': str(e)}, status=500)

def company_post(request):
    user = request.user  
    organization = Organization.objects.filter(login=user).first()
    posts = Post.objects.filter(login=request.user).order_by('-postdttime')  # Filter posts by logged-in user

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.login = request.user  # Assign logged-in user to the post
            post.save()
            return redirect('/company_post')

    else:
        form = PostForm()

    # 🔄 Fetch all comments with related post and user
    all_comments = Comments.objects.select_related('post', 'login').all()

    # Group comments by post ID
    comments_by_post = defaultdict(list)
    for c in all_comments:
        comments_by_post[c.post_id].append(c)

    return render(request,'company_post.html',{'user_id': user.id,
        'organization': organization,
        'posts': posts,
        'form':form,
        'comments_by_post': comments_by_post
        })

def agency_post(request):
    user = request.user  
    organization = Agency.objects.filter(login=user).first()
    posts = Post.objects.filter(login=request.user).order_by('-postdttime')  # Filter posts by logged-in user

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.login = request.user  # Assign logged-in user to the post
            post.save()
            return redirect('/agency_post')
            

    else:
        form = PostForm()

     # 🔄 Fetch all comments with related post and user
    all_comments = Comments.objects.select_related('post', 'login').all()

    # Group comments by post ID
    comments_by_post = defaultdict(list)
    for c in all_comments:
        comments_by_post[c.post_id].append(c)
    return render(request,'agency_post.html',{'user_id': user.id,
        'organization': organization,
        'posts': posts,
        'form':form,
        'comments_by_post': comments_by_post,
        })

def company_job(request):
    user = request.user  
    organization = Organization.objects.filter(login=user).first()
    jobs = Job.objects.filter(organization=organization) # Filter posts by logged-in user

    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            jobs = form.save(commit=False)
            jobs.login = request.user  # Assign logged-in user to the post
            jobs.save()
            return redirect('/company_jo')

    else:
        form = JobForm()

    return render(request,'company_job.html',{'user_id': user.id,
        'organization': organization,
        'jobs': jobs,
        'form':form,
        })

def agency_job(request):
    user = request.user  
    agency = Agency.objects.filter(login=user).first()
    jobs = Job.objects.filter(agency=agency) # Filter posts by logged-in user

    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            jobs = form.save(commit=False)
            jobs.login = request.user  # Assign logged-in user to the post
            jobs.save()
            return redirect('/agency_job')

    else:
        form = JobForm()

    return render(request,'agency_job.html',{'user_id': user.id,
        'agency':agency,
        'jobs': jobs,
        'form':form,
        })

def jobseeker_side(request):
    
    jobs = Job.objects.all()
    cities = City.objects.all()
    print("Received GET parameters:", request.GET)  # Debugging line

    jobs = Job.objects.all()


    selected_location = request.GET.get('location')
    if selected_location and selected_location != "--Select location--":
        print(f"Filtering jobs with location: {selected_location}")
        jobs = jobs.filter(city__id=selected_location)  # Ensure correct field reference

    selected_experience = request.GET.get('experience')

# Filter by Experience
    experience_map = {
        "0 - 3 years": (0, 3),
        "4 - 7 years": (4, 7),
        "8 - 10 years": (8, 10),
        "More than 10 years": (10, 50),
    }

    if selected_experience in experience_map:
        min_exp, max_exp = experience_map[selected_experience]
        jobs = jobs.filter(requiredexperience__range=(min_exp, max_exp))

    selected_jobtype = request.GET.get('jobtype')

    if selected_jobtype and selected_jobtype != "--Select Job type--":
        jobs = jobs.filter(jobtype=selected_jobtype)

    selected_position = request.GET.get('position')

    if selected_position and selected_position != "--Select Position--":
        jobs = jobs.filter(position=selected_position)




    user = request.user 
    member = Member.objects.filter(login=user).first()
    cities = City.objects.all()

    
    print("Filtered jobs count:", jobs.count())  # Debugging line
        # Assign colors dynamically
    colors = ['ibm', 'amazon', 'wipro', 'google', 'dribble']
    for job in jobs:
        job.color = colors[job.id % len(colors)]
    
    return render(request,'job_seeker_side.html',{'jobs':jobs,'colors':colors,'cities':cities,'member':member,'jobs': jobs, 'cities': cities,'selected_location': selected_location,'selected_position': selected_position, 'selected_experience': selected_experience,'selected_jobtype': selected_jobtype,})


def view_cv(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    user_id = request.user.id
    member = Member.objects.filter(login=user_id).first()

    if member is None:
        return redirect('/login')

    education = MemberEducation.objects.filter(member=member)
    skills = MemberSkills.objects.filter(member=member)
    experience = MemberExperience.objects.filter(member=member)
    languages = MemberLanguage.objects.filter(member=member)
    links = MemberLink.objects.filter(member=member)
    summary = Summary.objects.filter(member=member)

    return render(request, 'view_cv.html', {
        'member': member,
        'education': education,
        'skills': skills,  
        'experience': experience,
        'languages': languages,
        'links': links,
        'summary': summary
    })

def cv(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    user_id = request.user.id
    member = Member.objects.filter(login=user_id).first()

    if member is None:
        return redirect('/login')

    # Fetch existing data
    education = MemberEducation.objects.filter(member=member)
    skills = MemberSkills.objects.filter(member=member)
    experience = MemberExperience.objects.filter(member=member)
    languages = MemberLanguage.objects.filter(member=member)
    links = MemberLink.objects.filter(member=member)
    summary = Summary.objects.filter(member=member)
    # Process form submission
    if request.method == 'POST':
        
        if 'education_form' in request.POST:
            edu_form = MemberEducationForm(request.POST)
            if edu_form.is_valid():
                edu = edu_form.save(commit=False)
                edu.member = member  # Assign the logged-in member
                edu.save()
                return redirect('/cv')

        elif 'skills_form' in request.POST:
            skills_form = MemberSkillsForm(request.POST)
            if skills_form.is_valid():
                skill = skills_form.save(commit=False)
                skill.member = member
                skill.save()
                return redirect('/cv')

        elif 'experience_form' in request.POST:
            exp_form = MemberExperienceForm(request.POST)
            if exp_form.is_valid():
                exp = exp_form.save(commit=False)
                exp.member = member
                exp.save()
                return redirect('/cv')

        elif 'language_form' in request.POST:
            lang_form = MemberLanguageForm(request.POST)
            if lang_form.is_valid():
                lang = lang_form.save(commit=False)
                lang.member = member
                lang.save()
                return redirect('/cv')

        elif 'link_form' in request.POST:
            link_form = MemberLinkForm(request.POST)
            if link_form.is_valid():
                link = link_form.save(commit=False)
                link.member = member
                link.save()
                return redirect('/cv')
        
        elif 'summary_form' in request.POST:
            summary_form = SummaryForm(request.POST)
            if summary_form.is_valid():
                summary = summary_form.save(commit=False)
                summary.member = member
                summary.save()
                return redirect('/cv')

    
    # Initialize empty forms
    context = {
        'member': member,
        'education': education,
        'skills': skills,
        'experience': experience,
        'languages': languages,
        'links': links,
        'summary': summary,
        'summary_form' : SummaryForm(),
        'edu_form': MemberEducationForm(),
        'skills_form': MemberSkillsForm(),
        'exp_form': MemberExperienceForm(),
        'lang_form': MemberLanguageForm(),
        'link_form': MemberLinkForm()
    }
    return render(request, 'cv.html', context)

def new_profile(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    user_id = request.user.id
    member = Member.objects.filter(login=user_id).first()

    if member is None:
        return redirect('/login')

    education = MemberEducation.objects.filter(member=member)
    skills = MemberSkills.objects.filter(member=member)
    experience = MemberExperience.objects.filter(member=member)
    languages = MemberLanguage.objects.filter(member=member)
    links = MemberLink.objects.filter(member=member)
    summary = Summary.objects.filter(member=member)

    selected_position = None  # Ensure selected_position exists

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            member = form.save(commit=False)
            city_id = request.POST.get('city')
            position_name = request.POST.get('position')
            if city_id:
                try:
                    member.city = City.objects.get(id=city_id)  # Update city
                except City.DoesNotExist:
                    pass  # Handle invalid city ID gracefully
                if position_name:
                # Try to fetch or create the position
                    selected_position, created = Positions.objects.get_or_create(positionname=position_name.strip())
                    member.position = selected_position 
            member.save()
            return redirect('/profile')

    else:
        form = ProfileForm(instance=member)
        if member.position:
            selected_position = member.position  # Ensure selected position is set
    
    cities = City.objects.all()
    positions = Positions.objects.all()

    return render(request, 'new_profile.html', {
        'member': member,
        'education': education,
        'skills': skills,  
        'experience': experience,
        'languages': languages,
        'links': links,
        'summary': summary,
        'form': form,
        'cities': cities,
        'positions': positions,
        'selected_position': selected_position,  # Ensure it's passed
    })


def otp(request):
    return render(request,'otp.html')
def emp(request):  
    if request.method == "POST":  
        form = EmployeeForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()  
                return redirect('/show')  
            except:  
                pass  
    else:  
        form = EmployeeForm()  
    return render(request,'emp.html',{'form':form})  
def show(request):  
    employees = Employee.objects.all()  
    return render(request,"show.html",{'employees':employees})  
def edit(request, id):  
    employee = Employee.objects.get(id=id)  
    return render(request,'edit.html', {'employee':employee})  
def update(request, id):  
    employee = Employee.objects.get(id=id)  
    form = EmployeeForm(request.POST, instance = employee)  
    if form.is_valid():  
        form.save()  
        return redirect("/show")  
    return render(request, 'edit.html', {'employee': employee})  
def destroy(request, id):  
    employee = Employee.objects.get(id=id)  
    employee.delete()  
    return redirect("/show")

def apply(request):
    member = Member.objects.filter(login=request.user).first()
    jobid = request.GET.get("jobid")
    print("Job ID",jobid)
    if request.POST:
        

        job= Job.objects.get(id=request.POST.get('jobid'))
        appl = Application()
        appl.job = job
        appl.attachment = request.FILES.get('attachment')
        appl.member= Member.objects.filter(login = request.user).get()
        appl.applydate = date.today()
        appl.remarks = request.POST.get('remarks')
        appl.save()
        print(appl)
    return render(request,'apply_now.html',{'jobid':jobid,'member':member})  

def applied_jobs(request):
    member = Member.objects.filter(login=request.user).first()
    if not member:
        return render(request, 'applied_jobs.html', {'error': 'No member profile found.'})
    #applications = Application.objects.filter(Q(member=member) & Q(status=''))
    applications = Application.objects.filter(member=member)  # Fetch all applications
    shortlistapplications = applications.filter(status='ShortList')
    rejectedapplications = applications.filter(status='Reject')
    #applications = Application.objects.filter(member=member)  # OR
    #applications = Application.objects.filter(Q(member=member) & (Q(status='') | Q(status__isnull=True)))
    # shortlistapplications = Application.objects.filter(Q(member=member) & Q(status='ShortList'))
    #rejectedapplications = Application.objects.filter(Q(member=member) & Q(status='Reject'))
    return render(request,'applied_jobs.html',{'applications':applications,'shortlistapplications':shortlistapplications,'rejectedapplications':rejectedapplications,'member':member})



def state(request):  
    if request.method == "POST":  
        form = StateForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()  
                return redirect('/showstate')  
            except:  
                pass  
    else:  
        form = StateForm()  
    return render(request,'state_index.html',{'form':form})  
def showstate(request):  
    states = State.objects.all()  
    return render(request,"state_show.html",{'states':states})  
def editstate(request, id):  
    state = State.objects.get(id=id)  
    return render(request,'state_edit.html', {'state':state})  
def updatestate(request, id):  
    state = State.objects.get(id=id)  
    form = StateForm(request.POST, instance = state)  
    if form.is_valid():  
        form.save()  
        return redirect("/showstate")   
    else:
        error_list = form.errors
        print(error_list)
    return render(request, 'state_edit.html', {'state': state})  
def destroystate(request, id):  
    state = State.objects.get(id=id)
    state.delete()  
    return redirect("/showstate")

def cmpct(request):  
    if request.method == "POST":  
        form = CompanyCategoryForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()  
                return redirect('/showcmpct')  
            except:  
                pass  
    else:  
        form = CompanyCategoryForm()  
    return render(request,'cc_index.html',{'form':form})  
def showcmpct(request):  
    CompanyCategories = CompanyCategory.objects.all()  
    return render(request,"cc_show.html",{'CompanyCategories':CompanyCategories})  
def editcmpct(request, id):  
    companycategory = CompanyCategory.objects.get(id=id)  
    return render(request,'cc_edit.html', {'CompanyCategory':companycategory})  
def updatecmpct(request, id):  
    companycategory = CompanyCategory.objects.get(id=id)  
    form = CompanyCategoryForm(request.POST, instance = companycategory)  
    if form.is_valid():
        form.save()
        return redirect("/showcmpct")  
    return render(request, 'cc_edit.html', {'CompanyCategory': CompanyCategory})  
def destroycmpct(request, id):  
    companycategory = CompanyCategory.objects.get(id=id)  
    companycategory.delete()  
    return redirect("/showcmpct")

def lgn(request):  
    if request.method == "POST":  
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = User  
    else:  
        form = authlogin()  
    return render(request,'login_index.html',{'form':form})  
def showlogin(request):  
    logins = authlogin.objects.all()  
    return render(request,"login_show.html",{'logins':logins})  
def editlogin(request, id):  
    login = authlogin.objects.get(id=id)  
    return render(request,'login_edit.html', {'login':login})  
def updatelogin(request, id):  
    login = authlogin.objects.get(id=id)  
    form = authlogin(request.POST, instance = login)  
    if form.is_valid():  
        form.save()  
        return redirect("/showlogin")  
    return render(request, 'login_edit.html', {'login': login})  
def destroylogin(request, id):  
    login = authlogin.objects.get(id=id)  
    login.delete()  
    return redirect("/showlogin")

def pstn(request):  
    if request.method == "POST":  
        form = PositionsForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()  
                return redirect('/showpstn')  
            except:  
                pass  
    else:  
        form = PositionsForm()  
    return render(request,'pstns_index.html',{'form':form})  
def showpstns(request):  
    positions = Positions.objects.all()  
    return render(request,"pstns_show.html",{'positions':positions})  
def editpstns(request, id):  
    position = Positions.objects.get(id=id)  
    return render(request,'pstns_edit.html', {'position':position})  
def updatepstns(request, id):  
    position = Positions.objects.get(id=id)  
    form = PositionsForm(request.POST, instance = position)  
    if form.is_valid():  
        form.save()  
        return redirect("/showpstn")  
    return render(request, 'pstns_edit.html', {'position': position})  
def destroypstns(request, id):  
    position = Positions.objects.get(id=id)  
    position.delete()  
    return redirect("/showpstn")

def city(request):  
    if request.method == "POST":  
        form = CityForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()  
                return redirect('/showcity')  
            except:  
                pass  
    else:  
        form = CityForm()  
    return render(request,'city_index.html',{'form':form})  
def showcity(request):  
    cities = City.objects.all()  
    return render(request,"city_show.html",{'cites':cities})  
def editcity(request, id):  
    city = City.objects.get(id=id)  
    return render(request,'city_edit.html', {'city':city})  
def updatecity(request, id):  
    city = City.objects.get(id=id)  
    form = CityForm(request.POST, instance = city)  
    if form.is_valid():  
        form.save()  
        return redirect("/showcity")  
    return render(request, 'editcity.html', {'city': city})  
def destroycity(request, id):  
    city = City.objects.get(id=id)  
    city.delete()  
    return redirect("/showcity")

from django.shortcuts import render, redirect, get_object_or_404
from .models import MemberEducation, MemberSkills, MemberExperience, MemberLanguage, MemberLink , Summary

def delete_education(request, edu_id):
    edu = get_object_or_404(MemberEducation, id=edu_id)
    edu.delete()
    return redirect('/cv')

def delete_skill(request, skill_id):
    skill = get_object_or_404(MemberSkills, id=skill_id)
    skill.delete()
    return redirect('/cv')

def delete_experience(request, exp_id):
    exp = get_object_or_404(MemberExperience, id=exp_id)
    exp.delete()
    return redirect('/cv')

def delete_language(request, lang_id):
    lang = get_object_or_404(MemberLanguage, id=lang_id)
    lang.delete()
    return redirect('/cv')

def delete_link(request, link_id):
    link = get_object_or_404(MemberLink, id=link_id)
    link.delete()
    return redirect('/cv')

def delete_summary(request, sum_id):
    sum = get_object_or_404(Summary, id=sum_id)
    sum.delete()