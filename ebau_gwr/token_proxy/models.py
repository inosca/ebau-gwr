import uuid

from cryptography.fernet import Fernet
from django.conf import settings
from django.db import models


class FernetStringField(models.BinaryField):
    description = "Encrypted string data"

    @property
    def fernet_key(self):
        return Fernet(settings.GWR_FERNET_KEY)

    def encrypt(self, value):
        return self.fernet_key.encrypt(value.encode("utf-8"))

    def decrypt(self, value):
        return self.fernet_key.decrypt(value).decode()

    def from_db_value(self, value, *_):
        if value is None:
            return value
        return self.decrypt(value)

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if value is None:
            return value
        return self.encrypt(value)


class HousingStatCreds(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.CharField(max_length=255)
    group = models.IntegerField()
    username = models.CharField(max_length=255)
    password = FernetStringField()
    municipality = models.IntegerField()
