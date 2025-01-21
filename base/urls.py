from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from base.views import *


router = DefaultRouter()
router.register(r"services", ServiceViewSet)
router.register(r"packages", ServicePackageViewSet)
# router.register(r"documents", SecureDocumentViewSet, basename="document")


urlpatterns = [
    path("", include(router.urls)),
    path("consultations/", consultation_create_update, name="consultation-list-create"),
    path(
        "consultations/<int:pk>/",
        consultation_create_update,
        name="consultation-detail-update",
    ),
    path(
        "consultations/<int:pk>/delete/",
        consultation_delete,
        name="consultation-delete",
    ),
    path("clients/", client_list, name="client-list"),
    path("clients/<int:pk>/", client_detail, name="client-detail"),
    path(
        "clients/<int:pk>/full-profile/",
        client_full_profile,
        name="client-full-profile",
    ),
    path("clients/<int:pk>/services/", client_services, name="client-services"),
    path("clients/<int:pk>/documents/", client_documents, name="client-documents"),
    path(
        "clients/<int:pk>/appointments/",
        client_appointments,
        name="client-appointments",
    ),
    path("clients/<int:pk>/notes/", client_notes, name="client-notes"),
    path("clients/<int:pk>/payments/", client_payments, name="client-payments"),
    path("appointments/", all_appointments, name="all_appointments"),
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "request-reset-email/",
        RequestPasswordResetEmail.as_view(),
        name="request-reset-email",
    ),
    path(
        "password-reset/<uidb64>/<token>/",
        PasswordTokenCheckAPI.as_view(),
        name="password-reset-confirm",
    ),
    path(
        "password-reset-complete",
        SetNewPasswordAPIView.as_view(),
        name="password-reset-complete",
    ),
    # Client Bio data urls
    path(
        "clients/<int:client_id>/personal-information/",
        personal_information_view,
        name="personal-information",
    ),
    path(
        "clients/<int:client_id>/contact-details/",
        contact_details_view,
        name="personal-information",
    ),
    path(
        "clients/<int:client_id>/education-history/",
        education_list,
        name="personal-information",
    ),
    path(
        "clients/<int:client_id>/education-history/<int:pk>/",
        education_list,
        name="personal-details",
    ),
    path(
        "clients/<int:client_id>/employment-history/",
        employment_list,
        name="employment-history-list",
    ),
    path(
        "clients/<int:client_id>/employment-history/<int:pk>/",
        employment_list,
        name="employment-history-detail",
    ),
    path(
        "clients/<int:client_id>/qualifications/",
        qualification_detail,
        name="qualifications",
    ),
    path(
        "clients/<int:client_id>/documents/",
        client_documents,
        name="get-client-documents",
    ),
    path(
        "clients/<int:client_id>/documents/upload/",
        client_documents,
        name="client-documents",
    ),
    path(
        "clients/<int:client_id>/documents/<int:document_id>/",
        delete_client_document,
        name="update-client-document",
    ),
    path(
        "clients/<int:client_id>/documents/<int:document_id>/delete/",
        delete_client_document,
        name="delete-client-document",
    ),
    # Job & Service Application
    path("jobs/", jobs_view, name="jobs-list"),
    path(
        "clients/<int:client_id>/job-application/",
        client_job_application,
        name="employment-history-list",
    ),
    path(
        "clients/<int:client_id>/job-application/<int:document_id>/",
        client_job_application,
        name="update-client-document",
    ),
    # Applications
    path(
        "clients/<int:client_id>/applications/",
        application_list,
        name="application-list",
    ),
    path(
        "clients/<int:client_id>/applications/<int:pk>/",
        application_detail,
        name="application-detail",
    ),
    # Tickets
    path(
        "clients/<int:client_id>/tickets/",
        client_tickets,
        name="ticket-history",
    ),
    # Library
    path("library/", library_list, name="document-list"),
    path("library/upload/", library_upload, name="document-upload"),
    # Administration
    path("staff-members/", staff_members_view, name="staff-members-view"),
    path("admin/job-applications/", get_job_applications, name="job-application"),
    path("admin/all-applications/", get_all_applications, name="job-application"),
    path(
        "admin/client/<int:client_id>/",
        client_admin_detail,
        name="get_personal_information",
    ),
    path(
        "admin/personal-information/<int:client_id>/",
        get_personal_information,
        name="get_personal_information",
    ),
    path(
        "admin/contact-details/<int:client_id>/",
        get_contact_details,
        name="get_contact_details",
    ),
    path(
        "admin/education-history/<int:client_id>/",
        get_education_history,
        name="get_education_history",
    ),
    path(
        "admin/employment-history/<int:client_id>/",
        get_employment_history,
        name="get_employment_history",
    ),
    path(
        "admin/qualifications/<int:client_id>/",
        get_qualifications,
        name="get_qualifications",
    ),
    path("admin/documents/<int:client_id>/", get_documents, name="get_documents"),
]
