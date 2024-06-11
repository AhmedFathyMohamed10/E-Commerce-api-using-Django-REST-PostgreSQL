from rest_framework import serializers
from .models import Cart
from order.serializers import OrderSerializer

class CartSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True, read_only=True)
    user = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['user', 'orders']
        read_only_fields = ['user']

    def get_user(self, obj):
        return obj.user.username if obj.user else None

    def create(self, validated_data):
        user = self.context['request'].user  # Get the authenticated user from the request context
        cart, created = Cart.objects.get_or_create(user=user)  # Get or create the cart for the user
        order_serializer = OrderSerializer(data=validated_data.get('orders'), many=True, context=self.context)

        if order_serializer.is_valid():
            orders = order_serializer.save(user=user)  # Set the user for the order
            cart.orders.add(*orders)  # Add the newly created order to the cart
            cart.save()
            
        return cart
