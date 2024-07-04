from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import WorkRequest

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        assert self.request.user.is_authenticated  # for mypy to know that the user is authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("home")


user_redirect_view = UserRedirectView.as_view()

def validate_email(email):
  # Implement your email validation logic here (optional)
  # You can use a library like django-email-validator or regular expressions to validate email format
  import re
  email_regex = re.compile(r"^[^@]+@[^@]+\.[^@]+$")
  if not email_regex.match(email):
    return False
  return True 


def work_request(request):
  if request.method == 'POST':
    # Get form data
    selected_options = request.POST.getlist('options')
    name = request.POST['name']
    email = request.POST['email']

    # Basic validation (optional)
    if not selected_options:
      messages.error(request, 'Please select at least one design service.')
      return render(request, 'base.html')
    if not name:
      messages.error(request, 'Please enter your name.')
      return render(request, 'base.html')
    if not email or not validate_email(email):  
      messages.error(request, 'Please enter a valid email address.')
      return render(request, 'base.html')

    # Process form data
    work_request = WorkRequest.objects.create(
        name=name,
        email=email,
        selected_options=selected_options,  
    )
    work_request.save()

    messages.success(request, 'Work request submitted successfully!')
    return redirect('home')  

  # Render the form on GET request
  return render(request, 'base.html')


