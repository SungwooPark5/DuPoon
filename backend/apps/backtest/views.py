from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .strategies import get_static_allocation_strategy


# Create your views here.
class BacktestView(APIView):
    """
    API view to perform a backtest using a static allocation strategy.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Perform a backtest using the static allocation strategy.
        """
        try:
            user_id = request.user.id
            result = get_static_allocation_strategy(user_id)
            return Response(
                {"message": "Backtest completed successfully", "result": result},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"message": f"Error during backtest: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
