import json

import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST


@pytest.mark.parametrize(
    "value,status_code",
    [
        (json.dumps([{"key": "foo", "value": "bar"}]), HTTP_200_OK),
        (json.dumps([{"key": "int", "value": 5, "lookup": "gt"}]), HTTP_200_OK),
        (
            json.dumps(
                [{"key": "foo", "value": "bar"}, {"key": "baz", "value": "bla"}]
            ),
            HTTP_200_OK,
        ),
        (
            json.dumps([{"key": "foo", "value": "ar", "lookup": "contains"}]),
            HTTP_200_OK,
        ),
        (
            json.dumps([{"key": "foo", "value": "bar", "lookup": "asdfgh"}]),
            HTTP_400_BAD_REQUEST,
        ),
        (json.dumps([{"key": "foo"}]), HTTP_400_BAD_REQUEST),
        (json.dumps({"key": "foo"}), HTTP_400_BAD_REQUEST),
        ("foo", HTTP_400_BAD_REQUEST),
        ("[{foo, no json)", HTTP_400_BAD_REQUEST),
    ],
)
def test_json_value_filter(db, gwr_link_factory, admin_client, value, status_code):
    doc = gwr_link_factory(context={"foo": "bar", "baz": "bla", "int": 23})
    gwr_link_factory(context={"foo": "baz"})
    gwr_link_factory()
    url = reverse("gwrlink-list")
    resp = admin_client.get(url, {"filter[context]": value})
    assert resp.status_code == status_code
    if status_code == HTTP_200_OK:
        result = resp.json()
        assert len(result["data"]) == 1
        assert result["data"][0]["id"] == str(doc.pk)


@pytest.mark.parametrize("field,expected_amount", [("eproid", 2), ("local-id", 3)])
def test_gwr_link_filter(db, gwr_link_factory, field, expected_amount, admin_client):
    gwr_link_factory.create_batch(1)
    gwr_link_factory.create_batch(2, eproid="foo")
    gwr_link_factory.create_batch(3, local_id="foo")

    url = reverse("gwrlink-list")
    resp = admin_client.get(url, {f"filter[{field}]": "foo"})
    assert resp.status_code == HTTP_200_OK
    result = resp.json()
    assert len(result["data"]) == expected_amount
    assert all(i["attributes"][field] == "foo" for i in result["data"])
