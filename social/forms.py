from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm

from django import forms

from social.models import UserProfile,Posts,Comments,Stories

# Registration form
class RegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=["username","email","password1","password2"]
        
# Login Form
class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"})) 
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    
# Userprofile form
class UserProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        exclude=('user','following','block')
        
        widgets={
            "dob":forms.DateInput(attrs={"class":"form-control","type":"date"})
        }
        
# Postform
class PostForm(forms.ModelForm):
    class Meta:
        model=Posts
        fields=["title","post_image"]
        
class CommentForm(forms.ModelForm):
    class Meta:     
        model=Comments
        fields=["text"]  
        
class StoryForm(forms.ModelForm):
    class Meta:
        model=Stories
        fields=["title","post_image"]
          
        
 