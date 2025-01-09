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
    path('poster/', views.poster_render, name='poster'),
    path('create-checkout-session/', views.CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('payment/', views.payment_page, name='payment_page'),
    path('webhook/', views.StripeWebhookView.as_view(), name='stripe-webhook'),
    
    path('create-one-time-payment-session/', views.CreateOneTimePaymentSessionView.as_view(), name='create_one_time_payment_session'),
    # path('subscriptions/', views.OrderListView.as_view(), name='order-list'),
    # path('one-time-payments/', views.OneTimePaymentListView.as_view(), name='one-time-payment-list'),
]
