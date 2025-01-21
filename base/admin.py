from django.contrib import admin
from .models import *
from django.contrib.auth.forms import (
    AdminPasswordChangeForm,
    UserChangeForm,
    UserCreationForm,
)
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = (
        AdminPasswordChangeForm  # Enables password change functionality
    )

    # Fields to display in the user list in the admin
    list_display = ("email", "is_staff", "is_superuser", "is_active", "last_login")
    list_filter = ("is_staff", "is_superuser", "is_active")

    # Fieldsets for the User detail view
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal Info"), {"fields": ()}),  # Add personal info fields if needed
        (
            _("Permissions"),
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "is_active",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),  # Display as read-only
    )

    # Add read-only fields
    readonly_fields = ("last_login",)

    # Fieldsets for adding a new user
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_superuser",
                    "is_active",
                ),
            },
        ),
    )

    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )


# Register your User model with the custom admin
admin.site.register(User, UserAdmin)
admin.site.register(StaffMember)
admin.site.register(Consultation)
admin.site.register(PersonalInformation)
admin.site.register(Qualification)
admin.site.register(Document)
admin.site.register(JobApplication)
admin.site.register(Job)
admin.site.register(Application)
admin.site.register(Ticket)
admin.site.register(Library)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "phone_number",
        "nationality",
    )
    search_fields = ("first_name", "last_name", "phone_number", "passport_number")
    list_filter = ("nationality",)
    ordering = ("id",)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "base_price", "is_active")
    search_fields = ("name",)
    list_filter = ("is_active",)
    ordering = ("id",)


@admin.register(ServicePackage)
class ServicePackageAdmin(admin.ModelAdmin):
    list_display = ("id", "service", "name", "package_type", "price", "is_active")
    search_fields = ("name", "service__name")
    list_filter = ("package_type", "is_active")
    ordering = ("id",)


@admin.register(ClientService)
class ClientServiceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "client",
        "service_package",
        "start_date",
        "status",
        "total_amount",
        "amount_paid",
    )
    list_filter = ("status", "start_date")
    ordering = ("id",)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "client_service",
        "amount",
        "payment_date",
        "payment_method",
        "transaction_id",
    )
    search_fields = ("transaction_id",)
    list_filter = ("payment_method", "payment_date")
    ordering = ("id",)


admin.site.register(ClientDocument)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "client",
        "client_service",
        "appointment_type",
        "date_time",
        "status",
    )
    search_fields = ("appointment_type",)
    list_filter = ("status", "date_time")
    ordering = ("id",)


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "client",
        "client_service",
        "created_by",
        "created_at",
        "updated_at",
    )
    search_fields = ("content",)
    list_filter = ("created_at", "updated_at")
    ordering = ("id",)
