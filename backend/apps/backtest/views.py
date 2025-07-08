import bt

from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from common.utils import serialize_backtest_stats

from .strategies import get_static_allocation_strategy
from .serializers import BacktestSerializer, BacktestResultSerializer


# Create your views here.
class BacktestView(APIView):
    """
    API view to perform a backtest using a static allocation strategy.
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=BacktestSerializer,
        responses={
            200: BacktestResultSerializer,
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            500: "Internal Server Error",
        },
    )
    def post(self, request):
        """
        Perform a backtest using the static allocation strategy.
        """
        try:
            # 입력 검증
            serializer = BacktestSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            allocations = serializer.validated_data["allocations"]
            start_date = serializer.validated_data.get("start_date")
            end_date = serializer.validated_data.get("end_date")

            # 전략 실행
            backtest = get_static_allocation_strategy(
                allocations, start_date=start_date, end_date=end_date
            )
            result = bt.run(backtest)
            res = result[0]

            # 결과 직렬화 및 응답 반환
            data = serialize_backtest_stats(res)
            result_serializer = BacktestResultSerializer(data=data)
            result_serializer.is_valid(raise_exception=True)

            return Response(
                result_serializer.data,
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"message": f"Error during backtest: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
