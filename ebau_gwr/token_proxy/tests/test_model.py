import uuid

import pytest
from cryptography.fernet import Fernet
from django.db import connection, models

from ..models import FernetStringField


def get_fake_model(name):
    def get_test_model():
        meta_options = {"app_label": "token_proxy"}
        attributes = {
            "password": FernetStringField(null=True),
            "__module__": __name__,
            "__name__": name,
            "Meta": type("Meta", (object,), meta_options),
        }
        model = type(name, (models.Model,), attributes)
        return model

    model = get_test_model()

    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(model)

    return model


@pytest.mark.parametrize("pw", ["hunter2", "", None])
def test_fernet_password_field(db, settings, pw):
    model_name = str(uuid.uuid4()).replace("-", "")[:8]
    TestModel = get_fake_model(model_name)

    creds = TestModel.objects.create(password=pw)
    assert creds.password == pw

    # now check with value from db
    creds.refresh_from_db()
    assert creds.password == pw

    with connection.cursor() as cursor:
        cursor.execute('SELECT "password", "id" FROM %s' % f"token_proxy_{model_name}")
        row = cursor.fetchone()

    f = Fernet(settings.GWR_FERNET_KEY)
    if pw is None:
        assert row[0] is None
        return
    assert f.decrypt(row[0]).decode() == pw
