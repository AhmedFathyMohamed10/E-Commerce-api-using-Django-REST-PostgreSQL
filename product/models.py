from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
CHOICES = (
    ('electronics', 'Electronics'),
    ('fashion', 'Fashion'),
    ('home', 'Home'),
    ('beauty', 'Beauty'),
)
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    p_type = models.CharField(max_length=100, choices=CHOICES)

    def __str__(self):
        return self.name
    
    # --------------- Calculate stars on the fly --------------
    def total_stars(self):
        return self.reviews.aggregate(total=models.Sum('stars'))['total'] or 0

    def review_count(self):
        return self.reviews.count()

    def average_stars(self):
        review_count = self.review_count()
        if review_count > 0:
            return self.total_stars() / review_count
        return 0
    

class ProductLine(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.FloatField(default=0.00)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return str(self.product.name)
    

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/images/')

    def __str__(self):
        return str(self.product.name)
    


BRAND_CHOICES = (
    ('cotonile', 'Cotonile'),
    ('gucci', 'Gucci'),
    ('nike', 'Nike'),
    ('adidas', 'Adidas'),
)
class ProductBrand(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    brand = models.CharField(max_length=100, choices=BRAND_CHOICES)

    def __str__(self):
        return str(self.product.name)


