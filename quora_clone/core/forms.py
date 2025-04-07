from django import forms
from django.contrib.auth.models import User
from .models import Question,Answer
from django.contrib.auth.forms import UserCreationForm

class SignupForm(UserCreationForm):
    email = forms.EmailField(required = True)

    class Mets:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']  
        if commit:
            user.save()
        return user

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
