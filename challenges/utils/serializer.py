from typing import Any

from django.core import serializers
from django.db.models import QuerySet


def to_json(model_object: QuerySet, fields: tuple[str, ...] | None = None) -> Any:
    return serializers.serialize(
        "json",
        model_object,
        fields=fields,
        indent=2,
    )
