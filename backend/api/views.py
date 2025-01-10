from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from orders.models import Order
from .serializers import OrderSerializer



class PaidApiView(APIView):
    def post(self, request):
        try:
            order = Order.objects.get(pk=request.data.get('order_id'))
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if order.paid:
            return Response({'detail': 'Order is already paid.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = OrderSerializer(order, data=request.data)

        if serializer.is_valid():
            order.paid = request.data.get('is_paid', False)
            serializer.save()
            return Response({'detail': 'Successful payment.', 
                             'redirect_link': f"https://127.0.0.1:8001/orders/paid/{request.data.get('order_id')}/" }, status=status.HTTP_200_OK)
           
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)