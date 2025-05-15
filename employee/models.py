from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import date

class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    ename = models.CharField(max_length=100)
    eemail = models.EmailField()
    econtact = models.CharField(max_length=15)

    class Meta:
        db_table = "tblemployee"

    def __str__(self):
        return self.ename
class State(models.Model):
    id = models.AutoField(primary_key=True)
    sname = models.CharField(max_length=100)

    def __str__(self):
        return self.sname

    class Meta:
        db_table = "state"
class CompanyCategory(models.Model):
    id = models.AutoField(primary_key=True)
    ccname = models.CharField(max_length=100)

    def __str__(self):
        return self.ccname
    
    class Meta:
        db_table = "company_category"
class Positions(models.Model):
    id = models.AutoField(primary_key=True)
    positionname = models.CharField(max_length=100)
    companycategory = models.ForeignKey(CompanyCategory, on_delete=models.CASCADE)

    class Meta:
        db_table = "positions"

    def __str__(self):
        return self.positionname
class City(models.Model):
    id = models.AutoField(primary_key=True)
    cityname = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    class Meta:
        db_table = "city"
    
    def __str__(self):
        return self.cityname
    

class Organization(models.Model):
    id = models.AutoField(primary_key=True,unique=True)
    cmpname = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logos/',blank=True,null=True)
    strmobileno = models.CharField(max_length=20)
    website = models.URLField(max_length=200)
    state = models.ForeignKey(State, on_delete=models.CASCADE,null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    strstatus = models.CharField(max_length=100)
    ccid = models.ForeignKey(CompanyCategory, on_delete=models.CASCADE,null=True)
    cmp_strength = models.IntegerField(blank=True, null=True)
    login = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "organization"
    
    def __str__(self):
        return self.cmpname

class Agency(models.Model):
    id = models.AutoField(primary_key=True,unique=True)
    cmpname = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logos/',blank=True,null=True)
    strmobileno = models.CharField(max_length=20)
    website = models.URLField(max_length=200)
    state = models.ForeignKey(State, on_delete=models.CASCADE,null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    strstatus = models.CharField(max_length=100)
    login = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "agency"
    
    def __str__(self):
        return self.cmpname
    


class Overview(models.Model):
    id = models.AutoField(primary_key=True)  
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,null=True)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE,null=True)
    overview = models.TextField(max_length=1000)

    def __str__(self):
        return f"Overview of {self.overview}"

class Member(models.Model):
    id = models.AutoField(primary_key=True)
    position = models.CharField(max_length=100)
    login = models.ForeignKey(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)
    dateofbirth = models.DateField()
    address = models.CharField(max_length=100)
    strmobileno = models.CharField(max_length=10)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    strstatus = models.CharField(max_length=100)
    profile = models.ImageField(upload_to='profile/',null=True)

    class Meta:
        db_table = "member"
    
    def __str__(self):
        return self.firstname
    
class MemberEducation(models.Model):
    id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    passingyear = models.CharField(max_length=4)
    institute = models.CharField(max_length=100)
    grade = models.CharField(max_length=20)
    remark = models.CharField(max_length=20)

    class Meta:
        db_table = "membereducation"
class MemberSkills(models.Model):
    id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    skills = models.CharField(max_length=100)
    details = models.CharField(max_length=100)

    class Meta:
        db_table = "memberskills"
class MemberExperience(models.Model):
    id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    organizationname = models.CharField(max_length=100)
    worktitle = models.CharField(max_length=100)
    workdetails = models.CharField(max_length=100)
    startdate = models.DateField()
    enddate = models.DateField()
    totalmonthexperience = models.IntegerField()

    class Meta:
        db_table = "memberexperience"  
class MemberLanguage(models.Model):
    id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    language = models.CharField(max_length=100)

    class Meta:
        db_table = "memberlanguage"

    def _str_(self):
        return self.language
class MemberLink(models.Model):
    id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    link_name = models.CharField(max_length=100)
    link_url = models.URLField(max_length=255)

    class Meta:
        db_table = "memberlink"

    def _str_(self):
        return self.link_name
class Summary(models.Model):
    id = models.AutoField(primary_key=True)  
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    description = models.TextField(max_length=1000)
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    login = models.ForeignKey(User, on_delete=models.CASCADE)
    posttitle = models.CharField(max_length=100)
    postcontent = models.ImageField(upload_to='content/')
    postdesc = models.CharField(max_length=100,null=True)
    postdttime = models.DateTimeField(auto_now_add=True)
    like_count = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "post"
    
    def __str__(self):
        return self.posttitle 
class Job(models.Model):

    jobtype_choices = [
        ('full-time', 'Full Time'),
        ('part-time', 'Part Time'),
        ('internship', 'Internship'),
    ]


    id = models.AutoField(primary_key=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,null=True)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE,null=True)
    cmpname = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    noofvacancies = models.IntegerField() 
    requiredqualification = models.CharField(max_length=100)
    requiredexperience = models.CharField(max_length=100)
    jobdescription = models.CharField(max_length=3000)
    jobtype = models.CharField(max_length=100,choices=jobtype_choices, default='full-time')
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    applystartdate = models.DateField()
    lastdate = models.DateField()
    skillsrequired = models.CharField(max_length=100)
    posted_date = models.DateTimeField(auto_now_add=True)  # Add this field

    class Meta:
        db_table = "job"
        ordering = ['-posted_date']  # Always order by latest posted job
    
    def __str__(self):
        return self.cmpname
    
class Application(models.Model):
    id = models.AutoField(primary_key=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    applydate = models.DateField()
    status = models.CharField(max_length=100)
    remarks = models.CharField(max_length=100)
    attachment = models.FileField()

    class Meta:
        db_table = "application" 
class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    login = models.ForeignKey(User, on_delete=models.CASCADE)
    commentsdate = models.DateField(auto_now_add=True)
    comments = models.CharField(max_length=100)

    class Meta:
        db_table = "comments"
class Message(models.Model):
    id = models.AutoField(primary_key=True)
    fromlogin= models.ForeignKey(User, related_name='messages_sent', on_delete=models.CASCADE)
    tologin = models.ForeignKey(User, related_name='messages_received', on_delete=models.CASCADE)
    msg = models.CharField(max_length=100)
    msgdt = models.DateField()

    class Meta:
        db_table = "message"
class Likes(models.Model):
    id = models.AutoField(primary_key=True)
    login = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like_count = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "likes"

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    followed_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "follow"
        unique_together = ('follower', 'following')  # prevents duplicate follows

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"
