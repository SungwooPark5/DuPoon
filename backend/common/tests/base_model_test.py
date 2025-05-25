from django.test import TestCase
from django.db import models

from typing import Type, Protocol


class CRUDTestConfig(Protocol):
    model: Type[models.Model]
    sample_data: dict
    sample_data_update: dict


class CRUDTestMixin:
    model: models.Model = None
    sample_data: dict = {}
    sample_data_update: dict = {}

    def test_create(self: CRUDTestConfig) -> None:
        instance = self.model.objects.create(**self.sample_data)
        self.assertIsNotNone(instance.id, "Instance should be created with an ID.")
