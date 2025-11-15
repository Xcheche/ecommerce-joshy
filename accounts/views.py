# accounts/views.py


from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model
from django.contrib.auth import authenticate, login as auth_login,get_backends
from django.contrib.auth import logout as auth_logout

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  # keep this

# DO NOT import from base64
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from accounts.forms import CustomUserUpdateForm, ProfileUpdateForm, RegisterForm
from accounts.models import UserProfile
from accounts.token import account_activation_token
from django.db import transaction

from common.tasks import send_email, send_welcome_emails

User = get_user_model()

#--------------------- Registration view --------------------
@transaction.atomic
def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save(commit=False)
            # normalize email for your CustomUser (email is USERNAME_FIELD)
            user.email = (user.email or "").lower()
            user.is_active = False  # require activation
            user.save()

            # Activation email
            current_site = get_current_site(request)
            ctx = {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
                "scheme": "https" if request.is_secure() else "http",
            }

            # fire after commit (threaded inside helper)
            transaction.on_commit(lambda: send_email(
                subject="Activate your account",
                email_to=[user.email],
                html_template="emails/activation_email.html",
                context=ctx,
            ))

            messages.success(
                request,
                "Registration successful. Please check your email to activate your account.",
            )
            return redirect("home")
        else:
            messages.error(
                request, "Registration failed. Please correct the errors below."
            )
    return render(request, "accounts/register.html", {"form": form})




#---------------------------- Activation view----------------------



def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
    except Exception:
        uid = None

    user = None
    if uid:
        try:
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            user = None

    if user is not None and account_activation_token.check_token(user, token):
        if not user.is_active:
            user.is_active = True
            user.save()

        # ---- THE IMPORTANT PART ----
        # Option A: use the exact dotted path of your backend
        backend_path = "accounts.auth_backends.EmailOrUsernameBackend"

        # Option B (safer): derive from the actually loaded backends
        # backend_obj = next(iter(get_backends()))
        # backend_path = f"{backend_obj.__module__}.{backend_obj.__class__.__name__}"

        # Set it on the user and pass it explicitly
        user.backend = backend_path

        # ensure profile exists
        profile, _ = UserProfile.objects.get_or_create(user=user)

        # send welcome + owner notification after commit (threaded)
        transaction.on_commit(lambda: send_welcome_emails(user))
        auth_login(request, user, backend=backend_path)
        # -----------------------------

        messages.success(request, "Your account has been activated successfully!")
        return redirect("home")

    messages.error(request, "Activation link is invalid or has expired.")
    return redirect("home")

#-------------------------Login------------------------------
""" Authentication with email or username is handled by the custom auth backend."""

def login_view(request):
    if request.method == "POST":
        ident = (
            request.POST.get("username_or_email") or request.POST.get("username") or ""
        ).strip()
        password = request.POST.get("password") or ""

        user = authenticate(request, username=ident, password=password)
        if user is not None:
            auth_login(request, user)
            nxt = request.GET.get("next") or request.POST.get("next") or "home"
            return redirect(nxt)

        messages.error(request, "Invalid credentials or inactive account.")
        # fall through to re-render

    return render(request, "accounts/login.html")


#-------------------------Logout---------------------------

def logout_view(request):
    auth_logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("home")



#-------------------------------Dashboard/Profile------------------------------

def profile_view(request):
    """ View user profile. """
    return render(request, "accounts/profile.html")


#-------------------------------Edit Profile------------------------------
def edit_profile_view(request):
    # make sure a profile exists (signal should do this, but be defensive)
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        user_form = CustomUserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
        messages.error(request, "Please correct the errors below.")
    else:
        user_form = CustomUserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)

    return render(
        request,
        "accounts/edit_profile.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
        },
    )