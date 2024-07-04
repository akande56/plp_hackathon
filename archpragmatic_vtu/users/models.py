from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models

class User(AbstractUser):
    """
    Default custom user model for Archpragmatic_vtu.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})



class WorkRequest(models.Model):
  options = (
    ('app_design', 'App Design'),
    ('graphic_design', 'Graphic Design'),
    ('motion_design', 'Motion Design'),
    ('ux_design', 'UX Design'),
    ('webdesign', 'Web Design'),
    ('marketing', 'Marketing'),
  )
  name = models.CharField(max_length=255)
  selected_options = models.CharField(max_length=255)
  email = models.EmailField()
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.name} - {self.email}"

  def save(self, *args, **kwargs):
    # Combine selected options into a comma-separated string
    self.selected_options = ','.join(self.selected_options)
    super().save(*args, **kwargs)