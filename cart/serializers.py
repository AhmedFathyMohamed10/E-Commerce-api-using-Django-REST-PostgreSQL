from decimal import Decimal
from rest_framework import serializers
from .models import Cart
from order.serializers import OrderSerializer

class CartSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True, read_only=True)
    user = serializers.SerializerMethodField()
    total_amount = serializers.SerializerMethodField()  # New field to hold the total amount
    total_after_discount = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['user', 'orders', 'total_amount', 'total_after_discount']
        read_only_fields = ['user', 'total_amount', 'total_after_discount']

    def get_total_amount(self, obj):
        total_amount = sum(Decimal(order['total_price']) for order in obj.orders.values())
        return f'{total_amount} $'
    
    def get_total_after_discount(self, obj):
        total_amount = sum(Decimal(order['total_price']) for order in obj.orders.values())
        num_orders = obj.orders.count()
        if num_orders >= 2:
            discount_factor = Decimal('0.9')  # 10% discount
            total_after_discount = total_amount * discount_factor
            return f"Total after discount is: {total_after_discount} $"
        else:
            return f'We have discounted nothing from your total sales, you have only one order in your cart.'
        
        
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
