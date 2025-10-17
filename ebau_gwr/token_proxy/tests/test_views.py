import json

import pytest
from cryptography.fernet import Fernet
from django.urls import reverse
from rest_framework import status


@pytest.mark.parametrize(
    "data,success,error",
    [
        (
            {
                "username": "winstonsmith",
                "group": "1",
                "password": "goldstein",
                "municipality": 1444,
            },
            True,
            None,
        ),
        (
            {"username": "winstonsmith", "password": "goldstein"},
            False,
            'No "x-camac-group" header passed for "admin"',
        ),
        (
            {"username": "winstonsmith", "group": "2", "password": "goldstein"},
            False,
            'No housing stat credentials found for user "admin"',
        ),
        (
            {"username": "winstonsmith"},
            False,
            'No "x-camac-group" header passed for "admin"',
        ),
        (
            {"password": "goldstein", "group": "1"},
            False,
            'No housing stat credentials found for user "admin"',
        ),
    ],
)
def test_token_proxy(db, settings, admin_client, requests_mock, data, success, error):
    requests_mock.post(
        f"{settings.GWR_HOUSING_STAT_BASE_URI}/tokenWS/",
        json={"success": True, "token": "eyIMATOKEN"},
    )
    url = reverse("housingstattoken-list")

    group = data.get("group", None)
    headers = {"HTTP_X_CAMAC_GROUP": group} if group else {}
    resp = admin_client.post(
        url, data=json.dumps(data), content_type="application/json", **headers
    )
    if success:
        assert resp.status_code == status.HTTP_201_CREATED
        assert resp.json() == {
            "username": "winstonsmith",
            "token": "eyIMATOKEN",
            "municipality": data["municipality"],
        }
    else:
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert resp.json() == {
            "400": {
                "source": "internal",
                "reason": error,
            }
        }


@pytest.mark.parametrize(
    "housing_stat_creds__username,housing_stat_creds__password,housing_stat_creds__municipality,housing_stat_creds__group",
    [("winston_smith", "goldstein", 1344, 1)],
)
@pytest.mark.parametrize(
    "data,response_status,check_values",
    [
        (
            {"username": "winston_smith", "group": 1, "password": "hunter2"},
            status.HTTP_201_CREATED,
            True,
        ),
        (
            {"username": "winston_smith", "group": 2, "password": "hunter2"},
            status.HTTP_400_BAD_REQUEST,
            False,
        ),
        (
            {"username": "winstonsmith", "group": 2, "password": "hunter2"},
            status.HTTP_400_BAD_REQUEST,
            False,
        ),
        ({"username": "winstons_smith"}, status.HTTP_400_BAD_REQUEST, False),
        ({"password": "hunter2", "group": 1}, status.HTTP_201_CREATED, True),
        (
            {"password": "hunter2", "group": 1, "municipality": 3222},
            status.HTTP_201_CREATED,
            True,
        ),
        ({}, status.HTTP_400_BAD_REQUEST, False),
    ],
)
def test_token_proxy_success_existing_creds(
    db,
    settings,
    admin_client,
    requests_mock,
    housing_stat_creds,
    data,
    response_status,
    check_values,
):
    requests_mock.post(
        f"{settings.GWR_HOUSING_STAT_BASE_URI}/tokenWS/",
        json={"success": True, "token": "eyIMATOKEN"},
    )
    url = reverse("housingstattoken-list")

    group = data.get("group", None)
    headers = {"HTTP_X_CAMAC_GROUP": group} if group else {}

    resp = admin_client.post(
        url, data=json.dumps(data), content_type="application/json", **headers
    )

    assert resp.status_code == response_status

    if check_values:
        housing_stat_creds.refresh_from_db()
        for k, v in data.items():
            assert getattr(housing_stat_creds, k) == v


@pytest.mark.parametrize(
    "housing_stat_creds__username,housing_stat_creds__password,housing_stat_creds__municipality,housing_stat_creds__group",
    [("admin", "pw", 1344, 1)],
)
def test_token_proxy_external_error(
    db, settings, admin_client, requests_mock, housing_stat_creds
):
    requests_mock.post(
        f"{settings.GWR_HOUSING_STAT_BASE_URI}/tokenWS/",
        status_code=401,
        text="wrong creds",
    )
    url = reverse("housingstattoken-list")

    resp = admin_client.post(url, HTTP_X_CAMAC_GROUP=1)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.json() == {"401": {"reason": "wrong creds", "source": "external"}}


def test_token_proxy_remove_creds(db, settings, admin_client, requests_mock):
    requests_mock.post(
        f"{settings.GWR_HOUSING_STAT_BASE_URI}/tokenWS/",
        json={"success": True, "token": "eyIMATOKEN"},
    )
    url = reverse("housingstattoken-list")
    data = {"username": "testy", "password": "test", "municipality": 1234}
    resp = admin_client.post(
        url,
        data=json.dumps(data),
        content_type="application/json",
        HTTP_X_CAMAC_GROUP=1,
    )

    url = url + "/logout"
    resp = admin_client.post(url, content_type="application/json", HTTP_X_CAMAC_GROUP=1)
    assert resp.status_code == status.HTTP_204_NO_CONTENT

    resp = admin_client.post(url, content_type="application/json", HTTP_X_CAMAC_GROUP=1)
    assert resp.status_code == status.HTTP_404_NOT_FOUND


def test_token_proxy_invalid_token(
    db, settings, admin_client, admin_user, requests_mock
):
    requests_mock.post(
        f"{settings.GWR_HOUSING_STAT_BASE_URI}/tokenWS/",
        json={"success": True, "token": "eyIMATOKEN"},
    )
    url = reverse("housingstattoken-list")
    data = {
        "username": "test_GWR",
        "group": 1,
        "password": "secret-pw",
        "municipality": 1234,
    }
    headers = {"HTTP_X_CAMAC_GROUP": data.get("group")}
    resp = admin_client.post(
        url, data=json.dumps(data), content_type="application/json", **headers
    )
    assert resp.status_code == status.HTTP_201_CREATED

    # Change fernet key, invalidating the stored credentials
    settings.GWR_FERNET_KEY = Fernet.generate_key().decode()

    resp = admin_client.post(url, data=None, content_type="application/json", **headers)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.json() == {
        "400": {
            "reason": f'Stored credentials are invalid for "{admin_user.username}"',
            "source": "internal",
        }
    }

    # Can overwrite existing invalid credentials with valid credentials
    resp = admin_client.post(
        url, data=json.dumps(data), content_type="application/json", **headers
    )
    assert resp.status_code == status.HTTP_201_CREATED

    resp = admin_client.post(url, data=None, content_type="application/json", **headers)
    assert resp.status_code == status.HTTP_201_CREATED
