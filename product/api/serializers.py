from rest_framework import serializers
from product.models import BRAND_CHOICES, Category, Product, ProductLine, ProductImage, ProductBrand

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

    def validate_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("Category name should only contain letters.")
        if len(value) < 3:
            raise serializers.ValidationError("Category name should be at least 3 characters long.")
        return value

class ProductLineSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = ProductLine
        fields = ['id', 'category', 'price']

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return value

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']

    def validate_image(self, value):
        if value.size > 5 * 1024 * 1024:  # 5MB
            raise serializers.ValidationError("Image size should not exceed 5MB.")
        return value

    def validate(self, data):
        if not data['image'].name.endswith(('jpg', 'jpeg', 'png')):
            raise serializers.ValidationError("Only jpg, jpeg, and png formats are supported.")
        return data

class ProductBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBrand
        fields = ['id', 'brand']

    def validate_brand(self, value):
        valid_brands = [choice[0] for choice in BRAND_CHOICES]
        if value not in valid_brands:
            raise serializers.ValidationError(f"Brand must be one of the following: {', '.join(valid_brands)}")
        return value

    def validate(self, data):
        if ProductBrand.objects.filter(product=data['product'], brand=data['brand']).exists():
            raise serializers.ValidationError("This product already has the specified brand.")
        return data

class ProductSerializer(serializers.ModelSerializer):
    product_lines = ProductLineSerializer(source='productline_set', many=True, read_only=True)
    product_images = ProductImageSerializer(source='productimage_set', many=True, read_only=True)
    product_brands = ProductBrandSerializer(source='productbrand_set', many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'p_type', 'product_lines', 'product_images', 'product_brands']

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Product name should be at least 3 characters long.")
        return value

    def validate_description(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Product description should be at least 10 characters long.")
        return value
