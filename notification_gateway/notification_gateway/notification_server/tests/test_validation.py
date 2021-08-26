import pytest

from django.utils.translation import gettext_lazy as _
from notification_gateway.notification_server.validation import FieldsValidation, MultiIDsField, JsonField


class TestFieldsValidation:
    def test_validation(self):
        data = {
            "ids": [1],
            "type": "user",
            "provider": "mail",
            "message": {
                "title": "nothing",
                "description": "nothing"
            },
            "persist": True,
            "ttl": 7
        }

        form = FieldsValidation(data)
        assert form.is_valid()
        assert len(form.errors) == 0

    def test_invalid_id_validation(self):
        data = {
            "ids": [],
            "type": "user",
            "provider": "mail",
            "message": {
                "title": "nothing",
                "description": "nothing"
            },
            "persist": True,
            "ttl": 7
        }

        form = FieldsValidation(data)
        assert not form.is_valid()
        assert len(form.errors["ids"]) == 1
        assert form.errors["ids"][0] == _("This field is required.")

    def test_invalid_type_validation(self):
        data = {
            "ids": [1],
            "type": "notype",
            "provider": "mail",
            "message": {
                "title": "nothing",
                "description": "nothing"
            },
            "persist": True,
            "ttl": 7
        }

        form = FieldsValidation(data)
        assert not form.is_valid()
        assert len(form.errors["__all__"]) == 1
        assert form.errors["__all__"][0] == _("Please enter the valid type user/subscription")

    def test_invalid_ttl_validation(self):
        data = {
            "ids": [1],
            "type": "user",
            "provider": "mail",
            "message": {
                "title": "nothing",
                "description": "nothing"
            },
            "persist": True
        }

        form = FieldsValidation(data)
        assert not form.is_valid()
        assert len(form.errors) == 2
        assert form.errors["ttl"][0] == _("This field is required.")
        assert form.errors["__all__"][0] == _("Cannot persist data without time to live")

    def test_multi_id_field(self):
        form = MultiIDsField()
        value1 = form.to_python([1])
        value2 = form.to_python(None)
        assert value1 == [1]
        assert value2 == []

    def test_json_field(self):
        form = JsonField()
        value1 = form.to_python({"message": "Testing the fields"})
        value2 = form.to_python(None)
        assert value1 == {"message": "Testing the fields"}
        assert value2 == {}
