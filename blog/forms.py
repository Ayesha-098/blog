from django import forms
from .models import Post, User, Comment
from django.contrib.auth.forms import UserCreationForm
from allauth.account.forms import SignupForm


class CustomSignupForm(SignupForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, widget=forms.RadioSelect)

    def save(self, request):
        user = super().save(request)
        user.role = self.cleaned_data['role']
        user.save()
        return user

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }


class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  # assuming your Comment model has 'content' field
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your comment here...'
            })
        }