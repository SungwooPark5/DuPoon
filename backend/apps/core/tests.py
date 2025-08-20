import pytest

from django.urls import reverse
from django.test import Client


# Create your tests here.
def test_root_permanent_redirect_to_backtest():
    url = reverse("home")
    client = Client()
    response = client.get(url)

    assert response.status_code == 301
    assert response.url == reverse("backtest:backtest")
