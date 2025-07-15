import bt

from django.shortcuts import render
from django.views.generic import TemplateView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from common.utils import serialize_backtest_stats

from .services.strategies import get_static_allocation_strategy
from .services.dtos import BacktestConfig
from .serializers import BacktestSerializer, BacktestResultSerializer


# Create your views here.
class BacktestView(TemplateView):
    """
    View to render the backtest page.
    """

    template_name = "backtest/backtest.html"


class BacktestAPIView(APIView):
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

            config = BacktestConfig(
                allocations=serializer.validated_data["allocations"],
                strategy_name=serializer.validated_data.get(
                    "strategy_name", "Custom Allocation"
                ),
                start_date=serializer.validated_data.get("start_date"),
                end_date=serializer.validated_data.get("end_date"),
                rebalance_freq=serializer.validated_data.get("rebalance_freq"),
                slippage=serializer.validated_data.get("slippage", 0.0),
                include_cash=serializer.validated_data.get("include_cash", False),
                cash_ticker=serializer.validated_data.get("cash_ticker", "CASH"),
                cash_weight=serializer.validated_data.get("cash_weight", 0.0),
            )

            # 전략 실행
            backtest = get_static_allocation_strategy(config)
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
