from django.apps import AppConfig


class OrderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'order'

    def ready(self):
        from django.contrib.auth.models import User
        def get_cart_count(self):
            from .models import Cart
            return Cart.objects.filter(username=self).count()

        User.add_to_class("get_cart_count", get_cart_count)