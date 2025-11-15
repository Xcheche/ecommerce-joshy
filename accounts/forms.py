# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from accounts.models import CustomUser, UserProfile


#-------------Registration Form-----------------
class RegisterForm(UserCreationForm):
    # Make username optional (since USERNAME_FIELD is email)
    username = forms.CharField(required=False)
    email = forms.EmailField(
        required=True, help_text="Required. Enter a valid email address."
    )

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "phone_no",
            "password1",
            "password2",
        )

        # Optional: quick Tailwind-friendly widgets (tweak as you like)
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "input"}),
            "last_name": forms.TextInput(attrs={"class": "input"}),
            "phone_no": forms.TextInput(attrs={"class": "input"}),
        }

    # --- Validations (case-insensitive) ---
    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip().lower()
        if CustomUser.objects.filter(email__iexact=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email

    # --- Username is optional ---
    def clean_username(self):
        username = (self.cleaned_data.get("username") or "").strip()
        if username and CustomUser.objects.filter(username__iexact=username).exists():
            raise ValidationError("This username is already taken.")
        return username or None  # store None if left blank
# --- Phone number is optional ---
    def clean_phone_no(self):
        phone = (self.cleaned_data.get("phone_no") or "").strip()
        # Optional: add your own phone rules/length check here
        return phone or None

    # --- Save all fields onto the CustomUser ---
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"].lower()
        user.username = self.cleaned_data.get("username")  # may be None
        user.first_name = self.cleaned_data.get("first_name") or ""
        user.last_name = self.cleaned_data.get("last_name") or ""
        user.phone_no = self.cleaned_data.get("phone_no")

        if commit:
            user.save()
        return user



#-------------Login Form-----------------
# class LoginForm(forms.Form):
#     username = forms.CharField(
#         label="Email or Username",
#         widget=forms.TextInput(attrs={"class": "input", "placeholder": "Email or Username"}),
#     )
#     password = forms.CharField(
#         widget=forms.PasswordInput(attrs={"class": "input", "placeholder": "Password"})
#     )


#-----------------------Profile Update Form-----------------------


class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model =CustomUser
        # You can add other fields from CustomUser here
        fields = ["email", "username", "first_name", "last_name", "phone_no"]
        exclude = ["user"]  # Prevents 'user' from showing up in the form


class ProfileUpdateForm(forms.ModelForm):
    # This form handles the country and city fields
    # You might want to override the city field to make it a simple ChoiceField
    # for the initial form render before JavaScript takes over.

    class Meta:
        model = UserProfile
        # fields = "__all__"
        exclude = ["user"]