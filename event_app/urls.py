from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Home & Dashboard
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/events/", views.get_filtered_events, name="filtered-events"),  # Add this line


    # Event URLs (CRUD)
    path("events/", views.event_list, name="event_list"),
    path("events/<int:event_id>/", views.event_detail, name="event_detail"),
    path("events/create/", views.event_create, name="event_create"),
    path("events/<int:event_id>/update/", views.event_update, name="event_update"),
    path("events/<int:event_id>/delete/", views.event_delete, name="event_delete"),

    # Participant URLs (CRUD)
    path("participants/", views.participant_list, name="participant_list"),
    path("participants/<int:participant_id>/", views.participant_detail, name="participant_detail"),
    path("participants/create/", views.participant_create, name="participant_create"),
    path("participants/<int:participant_id>/update/", views.participant_update, name="participant_update"),
    path("participants/<int:participant_id>/delete/", views.participant_delete, name="participant_delete"),

    # Category URLs (CRUD)
    path("categories/", views.category_list, name="category_list"),
    path("category/<int:category_id>/", views.category_detail, name="category_detail"),
    path("category/create/", views.category_create, name="category_create"),
    path("category/<int:category_id>/update/", views.category_update, name="category_update"),
    path("category/<int:category_id>/delete/", views.category_delete, name="category_delete"),

    # Search Functionality
    path("search/", views.event_search, name="event_search"),
]

# Serve media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




