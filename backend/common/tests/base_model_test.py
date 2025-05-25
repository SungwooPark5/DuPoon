import pytest
from typing import Type
from django.db import models


class CRUDTestMixin:
    model: Type[models.Model]
    sample_data: dict
    sample_data_update: dict

    def test_create(self):
        instance = self.model.objects.create(**self.sample_data)
        assert instance.pk is not None
        for key, value in self.sample_data.items():
            assert getattr(instance, key) == value

    def test_read(self):
        instance = self.model.objects.create(**self.sample_data)
        retrieved_instance = self.model.objects.get(pk=instance.pk)
        assert retrieved_instance.pk == instance.pk
        for key, value in self.sample_data.items():
            assert getattr(retrieved_instance, key) == value

    def test_update(self):
        instance = self.model.objects.create(**self.sample_data)
        for key, value in self.sample_data_update.items():
            setattr(instance, key, value)
        instance.save()

        updated_instance = self.model.objects.get(pk=instance.pk)
        for key, value in self.sample_data_update.items():
            assert getattr(updated_instance, key) == value

    def test_delete(self):
        instance = self.model.objects.create(**self.sample_data)
        instance.delete()
        with pytest.raises(self.model.DoesNotExist):
            self.model.objects.get(pk=instance.pk)
