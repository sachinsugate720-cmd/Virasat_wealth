from django.contrib import admin

from .models import ConsultationRequest


@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "phone", "primary_goal", "user", "created_at")
    list_filter = ("primary_goal", "created_at")
    search_fields = ("full_name", "email", "phone", "user__username")
    readonly_fields = ("created_at", "updated_at")
