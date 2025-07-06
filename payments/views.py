import stripe
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response

stripe.api_key = settings.STRIPE_SECRET_KEY

@api_view(['POST'])
def create_subscription_session(request):
    plan = request.data.get("plan")  # "monthly" or "yearly"
    email = request.data.get("email")

    if not email or plan not in ["monthly", "yearly"]:
        return Response({"error": "Invalid plan or missing email"}, status=400)

    price_ids = {
        "monthly": "price_1Rht3HGBPprXqVx5XFsrRuE3",  # replace with your Stripe price ID
        "yearly": "price_1Rht3rGBPprXqVx5Mr2sxmyk"     # replace with your Stripe price ID
    }

    try:
        customer = stripe.Customer.create(email=email)

        session = stripe.checkout.Session.create(
            customer=customer.id,
            payment_method_types=["card"],
            line_items=[{"price": price_ids[plan], "quantity": 1}],
            mode="subscription",
            success_url="http://localhost:3000/success?session_iCHECKOUT_SESSION_IDd={}",
            cancel_url="http://localhost:3000/cancel",
        )

        return Response({"url": session.url})
    except Exception as e:
        return Response({"error": str(e)}, status=500)
