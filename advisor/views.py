from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import (
    AdvisorAuthenticationForm,
    AdvisorRegistrationForm,
    ConsultationRequestForm,
)
from .lead_export import LEADS_FILE, append_lead_row, ensure_leads_file

def home(request):
    consultation_form = ConsultationRequestForm()

    if request.method == "POST" and request.POST.get("form_type") == "consultation":
        if not request.user.is_authenticated:
            messages.error(request, "Please login to request a consultation.")
            return redirect(f"{reverse('login')}?next={reverse('home')}")

        consultation_form = ConsultationRequestForm(request.POST)
        if consultation_form.is_valid():
            consultation = consultation_form.save(commit=False)
            consultation.user = request.user
            consultation.save()
            append_lead_row(
                event_type="consultation",
                username=request.user.username,
                email=consultation.email,
                full_name=consultation.full_name,
                phone=consultation.phone,
                primary_goal=consultation.get_primary_goal_display(),
                message=consultation.message,
            )
            messages.success(
                request, "Consultation request submitted successfully. We will contact you soon."
            )
            return redirect("home")
        messages.error(request, "Please correct the highlighted errors and submit again.")

    return render(request, "home.html", {"consultation_form": consultation_form})


def _safe_next_url(request, fallback="home"):
    next_url = request.GET.get("next") or request.POST.get("next")
    if next_url and url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return next_url
    return fallback


def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    next_url = _safe_next_url(request)
    if request.method == "POST":
        form = AdvisorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful. You are now logged in.")
            return redirect(next_url)
    else:
        form = AdvisorRegistrationForm()

    return render(
        request,
        "register.html",
        {
            "form": form,
            "next": next_url if next_url != "home" else "",
        },
    )


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    next_url = _safe_next_url(request)
    if request.method == "POST":
        form = AdvisorAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            append_lead_row(
                event_type="login",
                username=user.username,
                email=user.email,
            )
            messages.success(request, "Login successful.")
            return redirect(next_url)
        messages.error(request, "Invalid username or password.")
    else:
        form = AdvisorAuthenticationForm(request)

    return render(
        request,
        "login.html",
        {
            "form": form,
            "next": next_url if next_url != "home" else "",
        },
    )


def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.info(request, "You have been logged out.")
    return redirect("home")


@user_passes_test(lambda user: user.is_staff)
def export_leads_csv(request):
    ensure_leads_file()

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="leads.csv"'
    response.write(LEADS_FILE.read_text(encoding="utf-8"))
    return response
