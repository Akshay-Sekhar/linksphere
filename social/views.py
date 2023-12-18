from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect,reverse

from django.views.generic import FormView,CreateView,TemplateView,View,UpdateView,DetailView,ListView

from social.forms import RegistrationForm,LoginForm,UserProfileForm,PostForm,CommentForm,StoryForm

from social.models import UserProfile,Posts

from django.contrib.auth import authenticate,login,logout

# Create your views here.

# class SignUpView(FormView):
#     template_name="register.html"
#     form_class=RegistrationForm
    
#     def post(self,request,*args, **kwargs):
#         form=RegistrationForm(request.POST)
#         if form.is_valid:
#             form.save()
#             return redirect("signup")
#         else:
#             return render(request,"register.html",{"form":form})

# Register
class SignUpView(CreateView):
    template_name="register.html"
    form_class=RegistrationForm
    
    def get_success_url(self):
        return reverse("signin")
    
# Login
class SignInView(FormView):
    template_name="login.html"
    form_class=LoginForm
    
    def post(self,request,*args, **kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user_object=authenticate(request,username=uname,password=pwd)
            if user_object:
                login(request,user_object)
                print("success")
                return redirect("index")
        print("Failed")
        return render(request,"login.html",{"form":form})   

class IndexView(CreateView,ListView):
    template_name="index.html"
    form_class=PostForm
    model=Posts
    context_object_name="data"
    
    def form_valid(self,form): #To add anything before saving
        form.instance.user=self.request.user #To add user
        return super().form_valid(form) 
    
    def get_success_url(self):
        return reverse("index")
    
    def get_queryset(self):
        blocked_profile=self.request.user.profile.block.all()
        blockedprofile_id=[pr.user.id for pr in blocked_profile]
        qs=Posts.objects.all().exclude(user__id__in=blockedprofile_id).order_by("-created_date")
        return qs
    
class SignOutView(View):
    def get(self,request,*args, **kwargs):
        logout(request)
        return redirect("signin")  
    
# To updatebprofile
class ProfileUpdateView(UpdateView):
    template_name="profile_add.html"
    form_class=UserProfileForm
    model=UserProfile
        
    def get_success_url(self):
        return reverse("index") 
  
# User profile
class ProfileDetailView(DetailView):
    template_name="profile_detail.html"
    model=UserProfile
    context_object_name="data"
    
class ProfileListView(View):
    def get(self,request,*args, **kwargs):
        qs=UserProfile.objects.all().exclude(user=request.user)
        return render(request,"profile_list.html",{"data":qs}) 
    
class FollowView(View):
    def post(self,request,*args, **kwargs):
        id=kwargs.get("pk")
        profile_object=UserProfile.objects.get(id=id)
        action=request.POST.get("action")
        if action=="follow":
            request.user.profile.following.add(profile_object)
        elif action=="unfollow":
            request.user.profile.following.remove(profile_object)    
        return redirect("index")         
    
# To like/dislike
class PostLikeView(View):
    def post(self,request,*args, **kwargs):
        id=kwargs.get("pk")
        post_object=Posts.objects.get(id=id)
        action=request.POST.get("action")
        if action=="like":
            post_object.liked_by.add(request.user)
        elif action=="dislike":
            post_object.liked_by.remove(request.user)
        return redirect("index")  
    
class CommentView(CreateView):
    template_name="index.html"
    form_class=CommentForm
    
    def get_success_url(self):
        return reverse("index")     
    
    def form_valid(self,form):
        id=self.kwargs.get("pk")
        post_object=Posts.objects.get(id=id)
        form.instance.user=self.request.user
        form.instance.post=post_object
        return super().form_valid(form)
    
# profile block view
class ProfileBlockView(View):
    def post(self,request,*args, **kwargs):
        id=kwargs.get("pk")
        profile_object=UserProfile.objects.get(id=id)
        action=request.POST.get("action")
        if action=="block":
            request.user.profile.block.add(profile_object)
        elif action=="unblock":
            request.user.profile.block.remove(profile_object) 
        return redirect("index")    
    
class StoryCreateView(View):
    def post(self,request,*args, **kwargs):
        form=StoryForm(request.POST,files=request.FILES)
        if form.is_valid():
            form.instance.user=request.user
            form.save()
            return redirect("index")
        return redirect("index")           
                 

            
    
