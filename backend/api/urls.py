from django.urls import path
from .views import MissingPersonDetailView, MissingPersonListView
from .views import NextOfKinDetailView, NextOfKinListView
from .views import UnidentifiedBodyListView, UnidentifiedBodyDetailView
from .views import MatchView , UsersListView , CustomUserDetailView
from . import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
# Swagger schema view configuration
schema_view = get_schema_view(
    openapi.Info(
        title="Missing Persons & Mortuary Management API Documentation",
        default_version="v1",
        description="This API allows interaction with the Missing Persons and Mortuary Management system. It provides endpoints to manage missing persons, next of kin records, unidentified bodies, mortuary staff, police stations, police officers, and related resources.",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
# API view URLs
urlpatterns = [
    path('missing_persons/', MissingPersonListView.as_view(), name='missing_person_list_view'),
    path('missing_persons/<int:id>/', MissingPersonDetailView.as_view(), name='missing_person_detail_view'),
    path('police_stations/', views.PoliceStationListView.as_view(), name='police_station_list_view'),
    path('police_stations/<int:id>/', views.PoliceStationDetailView.as_view(), name='police_station_detail_view'),
    path('mortuaries/', views.MortuaryListView.as_view(), name='mortuary_list_view'),
    path('mortuaries/<int:id>/', views.MortuaryDetailView.as_view(), name='mortuary_detail_view'),
    path('police_officers/', views.PoliceOfficerListView.as_view(), name='police_officer_list_view'),
    path('police_officers/<int:id>/', views.PoliceOfficerDetailView.as_view(), name='police_officer_detail_view'),
    path('mortuary_staff/', views.MortuaryStaffListView.as_view(), name='mortuary_staff_list_view'),
    path('mortuary_staff/<int:id>/', views.MortuaryStaffDetailView.as_view(), name='mortuary_staff_detail_view'),
    path('unidentified_bodies/', UnidentifiedBodyListView.as_view(), name='unidentified_body_list_view'),
    path('unidentified_bodies/<int:id>/', UnidentifiedBodyDetailView.as_view(), name='unidentified_body_detail_view'),
    path('nextofkin/<int:id>/', NextOfKinDetailView.as_view(), name='nextofkin-detail'),
    path('nextofkin/', NextOfKinListView.as_view(), name='nextofkin-list'),
    path('matches/', MatchView.as_view(), name='matches'),
    path('users/', UsersListView.as_view(), name='users_list_view'),
    path('users/<int:id>/', CustomUserDetailView.as_view(), name='user_detail_view'),

    # Swagger and Redoc URLs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

