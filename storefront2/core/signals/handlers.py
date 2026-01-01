from django.dispatch import receiver
from store.signals import order_created

@receiver(order_created)
def on_order_created(sender, **kwargs):
    """Handle actions to be taken when an order is created."""
    print(f"Order created signal received from {sender}. Order details: {kwargs.get('order')}")