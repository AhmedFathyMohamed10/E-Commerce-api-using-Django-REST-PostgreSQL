from django.shortcuts import get_object_or_404, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Review
from product.models import Product
from .serializers import ReviewSerializer

class ReviewCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk, format=None):
        product = get_object_or_404(Product, pk=pk)
        serializer = ReviewSerializer(data=request.data, context={'request': request, 'product': product})
        
        if serializer.is_valid():
            serializer.save(user=request.user)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ReviewGetView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)