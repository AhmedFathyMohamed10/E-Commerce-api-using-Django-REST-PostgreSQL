from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# ----------------------- FILTERS UPDATED ----------------------
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter
from product.models import Product, Category
from .serializers import ProductSerializer, CategorySerializer

# --------------------------------------------------------------
class CategoryList(APIView):
    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# ---------------------------------------------------------------

# ---------------------------------------------------------------
class ProductList(APIView):
    filter_backends = [DjangoFilterBackend]

    def get(self, request, format=None):
        queryset = Product.objects.all()

        # Apply filters
        filterset = ProductFilter(request.GET, queryset=queryset)
        if filterset.is_valid():
            queryset = filterset.qs

        filtered_count = queryset.count()
    all_count = Product.objects.all().count()
        message = f"We found {filtered_count} out of {all_count} products."

        serializer = ProductSerializer(queryset, many=True)
        response_data = {
            'message': message,
            'data': serializer.data
        }
        return Response(response_data)

    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetail(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Response({'status': 'Product not found here.'}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        product = self.get_object(pk)
        if isinstance(product, Response):
            return product
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# ---------------------------------------------------------------