from django.contrib import admin

from chatapp import models

# Register your models here.

admin.site.register(models.ChatThread)
admin.site.register(models.ChatHistory)
admin.site.register(models.UserSubscription)
admin.site.register(models.UserPayment)
@admin.register(models.OneTimePayment)
class OneTimePaymentAdmin(admin.ModelAdmin):
    list_display = ('order_reference', 'payment_id', 'amount', 'currency', 'payment_status', 'user_email', 'customer_name', 'payment_date')

