import stripe
from django.conf import settings
import pdb
from django.views import View
from .models import Price
from django.shortcuts import redirect

from django.views.generic import TemplateView

from .models import Product

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        price = Price.objects.get(id=self.kwargs["pk"])
        payment = ''
        if price.stripe_price_id == 'price_1KRpL4Cor9GAAV0a3QvNlRuK':
            payment = 'subscription'
        else:
            payment = 'payment'

        YOUR_DOMAIN = "http://127.0.0.1:8000"

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': price.stripe_price_id,
                    'quantity': 1,
                },
            ],
            mode=payment,
            success_url=YOUR_DOMAIN + '/products/success/',
            cancel_url=YOUR_DOMAIN + '/products/cancel/',
        )

        return redirect(checkout_session.url)


class SuccessView(TemplateView):
    template_name = "success.html"


class CancelView(TemplateView):
    template_name = "cancel.html"


class ProductLandingPageView(TemplateView):
    template_name = "landing.html"

    def get_context_data(self, **kwargs):
        product = Product.objects.get(name="Test Product")
        prices = Price.objects.filter(product=product)
        context = super(ProductLandingPageView, self).get_context_data(**kwargs)

        context.update({
            "product": product,
            "prices": prices
        })

        return context
