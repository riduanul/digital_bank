from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, FormView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserRegistrationForm, UserUpdateForm
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string 
# Create your views here.


def send_transaction_email(user, subject, template ):
        message = render_to_string(template, {
            'user':user,
            
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, 'text/html')
        send_email.send()

class UserRegistrationView(FormView):
    template_name = 'accounts/user_registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('profile')
    
    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, 'Registration Successful ')
        login(self.request, user)
        return super().form_valid(form) #form valid functionta call hobe jodi sob thik thake


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    def get_success_url(self):
        messages.success(self.request, 'Logged in Successfully ')
        return reverse_lazy('home')
    


class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('home')

class UserProfileUpdateView(UpdateView):
    template_name = 'accounts/profile.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the user's profile page
        return render(request, self.template_name, {'form': form})


def password_change(request):
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST )
            if form.is_valid():
                form.save()
                messages.success(request, 'Password Updated Successfully ')
                update_session_auth_hash(request, form.user)
                send_transaction_email(request.user,"Password Change Message",'password_email.html' )
                return redirect('profile')
        else:
            form = PasswordChangeForm(request.user)

        return render(request, 'password_change.html', {'form': form})



    
    
    
    
    