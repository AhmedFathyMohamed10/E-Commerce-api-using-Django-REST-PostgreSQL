from rest_framework import serializers

from cart.models import Cart
from product.models import ProductLine
from .models import Order, OrderItem, ShippingAddress, OrderStatus
from product.api.serializers import ProductSerializer

class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = ['country', 'state', 'city', 'postal_code']
        read_only_fields = ['user']

    def validate_postal_code(self, value):
        if len(value) < 4:
            raise serializers.ValidationError("Postal code must be at least 4 characters long.")
        return value

    def validate(self, data):
        if not data.get('country') or not data.get('state') or not data.get('city'):
            raise serializers.ValidationError("Country, state, and city must be provided.")
        return data


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(
        read_only=True
    )
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']
        read_only_fields = ['price', 'product']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value
    

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    shipping_address = ShippingAddressSerializer()

    class Meta:
        model = Order
        fields = ['id', 'status', 'shipping_address', 'created_at', 'updated_at', 'total_price', 'items']
        read_only_fields = ['user']  # Marking user field as read-only

    
    def create(self, validated_data):
        user = self.context['request'].user  # Getting the user from request context
        items_data = validated_data.pop('items')
        
        shipping_address_data = validated_data.pop('shipping_address')
        shipping_address = ShippingAddress.objects.create(user=user, **shipping_address_data)
        
        order = Order.objects.create(shipping_address=shipping_address, **validated_data)

        total_price = 0
        for item_data in items_data:
            product = item_data['product']
            product_line = ProductLine.objects.get(product=product)  # Get the ProductLine associated with the product

            # Check if the stock is sufficient
            if product_line.stock < item_data['quantity']:
                raise serializers.ValidationError(f"Insufficient stock for product {product.name}")

            item_price = product_line.price * item_data['quantity']  # Calculate the item price from the ProductLine
            item_data['price'] = item_price
            OrderItem.objects.create(order=order, **item_data)
            total_price += item_price

            # Reduce the stock
            product_line.stock -= item_data['quantity']
            product_line.save()

        order.total_price = total_price
        order.save()

        # Add order to the user's cart
        cart, created = Cart.objects.get_or_create(user=user)
        cart.orders.add(order)
        cart.save()
        
        return order
    