from datetime import datetime
from django.db.models import Q
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404

from .models import Product, Price
from .serializers import ProductSerializer, PriceSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, `update` and `destroy` actions.
    Additionally, it provides a custom `detailed_info` action.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['get'])
    def detailed_info(self, request, pk=None):
        product = self.get_object()
        current_price = product.price.latest('start_date').price if product.price.exists() else None
        price_history = list(product.price.values('start_date',"end_date",'price'))

        return Response({
            "product_name": product.name,
            "current_price": current_price,
            "price_history": price_history
        })


class PriceViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, `update` and `destroy` actions.
    Additionally, it provides a custom `average_price` action.
    """
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('from_date', openapi.IN_QUERY,
                              description="Start date of the price range (inclusive), format: YYYY-MM-DD",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('to_date', openapi.IN_QUERY,
                              description="End date of the price range (inclusive), format: YYYY-MM-DD",
                              type=openapi.TYPE_STRING)
        ]
    )
    @action(detail=True, methods=['get'])
    def average_price(self, request, pk=None):
        from_date_str = request.query_params.get('from_date')
        to_date_str = request.query_params.get('to_date')
        
        try:
            from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date() if from_date_str else None
            to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date() if to_date_str else None
        except ValueError:
            return Response({"error": "Invalid date format. Please use 'YYYY-MM-DD'."}, status=400)

        product = get_object_or_404(Product, pk=pk, user=request.user)

        query_conditions = Q(product=product)
        if from_date and to_date:
            query_conditions &= Q(start_date__lte=to_date) & (Q(end_date__gte=from_date) | Q(end_date__isnull=True))
        elif from_date:
            query_conditions &= Q(end_date__gte=from_date) | Q(end_date__isnull=True)
        elif to_date:
            query_conditions &= Q(start_date__lte=to_date)

        prices = Price.objects.filter(query_conditions)

        total_price = 0
        total_days = 0
        for price in prices:
            adjusted_start_date = max(price.start_date, from_date) if from_date else price.start_date
            adjusted_end_date = price.end_date if price.end_date else price.start_date

            days = (adjusted_end_date - adjusted_start_date).days + 1
            total_price += days * price.price
            total_days += days
        if total_days > 0:
            average_price = total_price / total_days
            return Response({"average_price": round(average_price, 2)})
        else:
            return Response({"error": "No prices found in the given date range."}, status=400)
