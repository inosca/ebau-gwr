from rest_framework.exceptions import ValidationError
from rest_framework_json_api import serializers

from . import models
from .client import HousingStatClient


class TokenProxySerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    group = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)
    municipality = serializers.IntegerField(required=False)
    token = serializers.SerializerMethodField()

    def get_token(self, obj):
        # No password or invalid password stored
        if not obj.password:
            raise ValidationError(
                {
                    400: {
                        "source": "internal",
                        "reason": f'Stored credentials are invalid for "{obj.owner}"',
                    }
                }
            )

        client = HousingStatClient()
        token_resp = client.get_token(username=obj.username, password=obj.password)
        if token_resp["success"] is True:
            return token_resp["token"]
        raise ValidationError(
            {
                token_resp["status_code"]: {
                    "source": "external",
                    "reason": token_resp["reason"],
                }
            }
        )

    def create(self, validated_data):
        user = self.context["request"].user
        try:
            group = self.context["request"].headers["x-camac-group"]
        except KeyError:
            raise ValidationError(
                {
                    400: {
                        "source": "internal",
                        "reason": f'No "x-camac-group" header passed for "{user.username}"',
                    }
                }
            )

        username = validated_data.get("username")
        password = validated_data.get("password")
        municipality = validated_data.get("municipality")

        if username and password and municipality:
            user_creds, _ = models.HousingStatCreds.objects.update_or_create(
                owner=user.username,
                group=group,
                defaults={
                    "username": username,
                    "password": password,
                    "municipality": municipality,
                },
            )
        else:
            user_creds = models.HousingStatCreds.objects.filter(
                owner=user.username, group=group
            )
            user_creds.update(**validated_data)
            user_creds = user_creds.first()
            if not user_creds:
                raise ValidationError(
                    {
                        400: {
                            "source": "internal",
                            "reason": f'No housing stat credentials found for user "{user.username}"',
                        }
                    }
                )

        return user_creds

    class Meta:
        model = models.HousingStatCreds
        fields = ("username", "group", "password", "token", "municipality")
