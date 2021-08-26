from django import forms
import json


class MultiIDsField(forms.Field):
    def to_python(self, value):
        """Normalize data to a list of strings."""
        # Return an empty list if no input was given.
        if not value:
            return []
        return value


class JsonField(forms.Field):
    def to_python(self, value):
        if not value:
            return {}
        return value


class FieldsValidation(forms.Form):
    ids = MultiIDsField()
    type = forms.CharField(max_length=225)
    provider = forms.CharField(max_length=225)
    message = JsonField()
    persist = forms.BooleanField()
    ttl = forms.IntegerField()

    def clean(self):
        cleaned_data = super().clean()
        persist = cleaned_data.get("persist")
        ttl = cleaned_data.get("ttl")
        ids = cleaned_data.get("ids")
        type = cleaned_data.get("type")

        if type != "user" and type != "subscription":
            raise forms.ValidationError("Please enter the valid type user/subscription")

        if persist and not ttl:
            raise forms.ValidationError("Cannot persist data without time to live")


