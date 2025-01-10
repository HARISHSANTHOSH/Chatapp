import logging
from datetime import datetime

import stripe
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.timezone import make_aware
from django.views.decorators.csrf import csrf_exempt
from rest_framework import response, status
from rest_framework.response import Response

from chatapp import send_mail

from . import models
from .exceptions import CustomException

logger = logging.getLogger(__name__)


class StripeWebhookHandler:

    @staticmethod
    def verify_webhook(payload, sig_header, cli_secret, webhook_secret):
        """Verify the webhook using CLI and webhook secrets."""
        try:
            event = None
            try:
                event = stripe.Webhook.construct_event(
                    payload, sig_header, cli_secret
                )
                logger.info("Webhook verified with CLI secret")
            except stripe.error.SignatureVerificationError:
                try:
                    event = stripe.Webhook.construct_event(
                        payload, sig_header, webhook_secret
                    )
                    logger.info("Webhook verified with webhook secret")
                except stripe.error.SignatureVerificationError as e:
                    logger.error(f"Signature verification failed: {str(e)}")
                    return JsonResponse(
                        {"error": "Invalid signature"}, status=400
                    )
            return event
        except Exception as e:
            logger.error(
                f"Webhook verification error: {str(e)}", exc_info=True
            )
            return JsonResponse({"error": str(e)}, status=500)

    @staticmethod
    def handle_checkout_session(event):
        """Handle the 'checkout.session.completed' event."""
        try:
            # Extract data from the session object
            session = event["data"]["object"]
            plan_id = session["metadata"].get("plan_id", "unknown")
            amount_received = (
                session.get("amount_total", 0) / 100
            )  # Convert cents to dollars
            currency = session.get("currency", "usd")
            order_reference = session.get("client_reference_id")
            payment_status = session["payment_status"]
            timestamp = session.get("created", None)
            payment_date = make_aware(datetime.fromtimestamp(timestamp))
            customer_details = session.get("customer_details", {})
            customer_email = customer_details.get("email", "")
            customer_name = customer_details.get("name", "")

            now = timezone.now()
            start_date = now - relativedelta(months=1)
            current_period_end = now + relativedelta(months=1)
            subscription_id = session.get("subscription")
            subscription = stripe.Subscription.retrieve(subscription_id)
            latest_invoice_id = subscription.latest_invoice
            invoice = stripe.Invoice.retrieve(latest_invoice_id)
            payment_intent_id = invoice.payment_intent
            logger.info("payment_intent_id:", payment_intent_id)

            # Check if the order has already been processed
            if models.UserSubscription.objects.filter(
                order_reference=order_reference
            ).exists():
                logger.info(
                    f"Order reference {order_reference} already exists. Skipping creation."
                )
                return Response(
                    {"status": "Order already processed"},
                    status=status.HTTP_200_OK,
                )

            # Check if the user already has an existing subscription
            existing_subscription = models.UserSubscription.objects.filter(
                user_email=customer_email
            ).first()

            # If the user has an existing subscription, it's an upgrade or change
            if existing_subscription:
                # If the plan has changed, mark the old subscription as upgraded
                if existing_subscription.plan != plan_id:
                    existing_subscription.status = "inactive"
                    existing_subscription.save()

                # Create a new subscription for the upgraded plan
                user_subscription = models.UserSubscription.objects.create(
                    user_email=customer_email,
                    customer_name=customer_name,
                    order_reference=order_reference,
                    plan=plan_id,
                    status="active",  # New subscription is active
                    start_date=start_date,
                    current_period_end=current_period_end,
                )

                # Log the upgrade event
                logger.info(
                    f"Subscription upgraded for {customer_email}, Plan: {plan_id}"
                )

                # Send an upgrade email if needed (optional)
                # send_mail.send_upgrade_email(user_subscription)

            else:
                # No existing subscription, create a new one (for a new user)
                user_subscription = models.UserSubscription.objects.create(
                    user_email=customer_email,
                    customer_name=customer_name,
                    order_reference=order_reference,
                    plan=plan_id,
                    status="active",  # New subscription is active
                    start_date=start_date,
                    current_period_end=current_period_end,
                )

                # Log the new subscription creation
                logger.info(
                    f"New subscription created for {customer_email}, Plan: {plan_id}"
                )
                # Send a confirmation email if needed (optional)
                # send_mail.send_subscription_confirmation(user_subscription)

            # Create a payment record in the UserPayment model
            user_payment = models.UserPayment.objects.create(
                user_subscription=user_subscription,
                payment_id=payment_intent_id,
                amount=amount_received,
                currency=currency,
                payment_status=payment_status,
                payment_date=payment_date,
            )

            return Response(
                {"status": "Subscription created/updated successfully"},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            # Log any errors that occur during processing
            logger.error(
                f"Error processing checkout session: {str(e)}", exc_info=True
            )
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


    @staticmethod
    def handle_payment_intent(event):
        """Handle the 'payment_intent.succeeded' event for one-time custom payments."""
        try:
            payment_intent = event["data"]["object"]
            print(payment_intent)

            # Extract payment details
            order_reference = payment_intent["metadata"].get("order_reference")
            amount_received = (
                payment_intent.get("amount_total", 0) / 100
            )  # Convert cents to dollars
            currency = payment_intent.get("currency", "usd")
            payment_status = payment_intent.get("status", "unknown")
            payment_id = payment_intent.get("payment_intent")
            payment_date = timezone.now()
            print("pa", payment_date)

            # Get customer details if available
            customer_details = payment_intent.get("customer_details", {})
            user_email = customer_details.get("email")
            customer_name = customer_details.get("name")

            # Check if payment already processed
            if models.OneTimePayment.objects.filter(
                order_reference=order_reference
            ).exists():
                # Raise the custom exception for duplicate payment
                return response.Response(
                    {"status": "Order already processed"},
                    status=status.HTTP_200_OK,
                )

            # Create payment record
            models.OneTimePayment.objects.create(
                order_reference=order_reference,
                payment_id=payment_id,
                amount=amount_received,
                currency=currency,
                payment_status=payment_status,
                payment_date=payment_date,
                user_email=user_email,
                customer_name=customer_name,
            )

            return response.Response(
                {
                    "result": True,
                    "message": "Payment processed successfully. Payment record created.",
                },
                status=status.HTTP_200_OK,
            )

        except CustomException as e:
            # Handle the custom exception (for duplicate payment)
            return response.Response(
                {
                    "result": e.detail["result"],
                    "message": e.detail["msg"],
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            # Handle database errors or other unexpected errors
            if isinstance(e, models.OneTimePayment.DoesNotExist):
                logger.error(f"Database error: {str(e)}")
                raise CustomException(
                    detail={
                        "result": False,
                        "msg": f"Database error occurred: {str(e)}",
                    }
                )
            else:
                # Log general unexpected errors
                logger.error(
                    f"Payment intent handling error: {str(e)}", exc_info=True
                )
                raise CustomException(
                    detail={
                        "result": False,
                        "msg": f"An unexpected error occurred: {str(e)}",
                    }
                )
