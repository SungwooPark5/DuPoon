import pytest
import json

from channels.testing import WebsocketCommunicator

from apps.stock.consumers import PriceUpdateConsumer
from config.asgi import application


@pytest.mark.asyncio
class TestPriceUpdateConsumer:
    @pytest.fixture
    def user(self, django_user_model):
        return django_user_model.objects.create_user(
            username="testuser", password="testpass"
        )

    async def test_user_can_connect_to_websocket(self, user):
        """
        communicator = WebsocketCommunicator(
            PriceUpdateConsumer.as_asgi(),
            path=f"/ws/price-update/{user.id}",
        )

        위와 같은 방식으로 할 경우, URLRoute를 하지 않은 단위 테스트가 됨
        때문에 consumer 내부에서 scope를 호출할 경우, 정보가 없기 때문에
        오류가 발생함. 단위 테스트를 하고 싶을 경우 mocking을 하여 scope와
        channel_name 등 필요한 정보를 직접 주입할 필요가 있음

        아래의 경우는 Router를 사용하였기 때문에 asgi router가 포함된
        통합 테스트라고 할 수 있음
        """
        communicator = WebsocketCommunicator(
            application=application,
            path=f"/ws/price-update/{user.id}",
        )

        connected, subprotocol = await communicator.connect()
        assert connected

        await communicator.disconnect()
