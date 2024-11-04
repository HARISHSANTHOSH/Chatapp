from django.urls import path

from . import views

urlpatterns = [
    path("chat/", views.ChatHistory.as_view(), name="chat"),
    path(
        "chat/<str:thread_id>/",
        views.ChatHistory.as_view(),
        name="get_chat_conversations",
    ),
    path("thread/", views.ChatThread.as_view(), name="chat_threads"),
    path("bookmark/", views.ChatBookmark.as_view(), name="chat_bookmark"),
]
