from rest_framework import serializers
from .models import Review
from product.models import Product


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    username = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['user', 'username', 'review_text', 'stars', 'created_at']
        read_only_fields = ['created_at']

    def validate_stars(self, value):
        if value < 0 or value > 5:
            raise serializers.ValidationError("Stars must be between 0 and 5")
        return value
    
    def validate(self, data):
        user = self.context['request'].user
        product = self.context['product']
        if Review.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError("You have already reviewed this product")
        return data
    
    def get_username(self, obj):
        return obj.user.username if obj.user else None

    def create(self, validated_data):
        product = self.context['product']
        return Review.objects.create(product=product, **validated_data)