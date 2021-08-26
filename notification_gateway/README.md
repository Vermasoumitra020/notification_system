# Notification Gateway Service

Exposes API to the client to send notifications.


## Settings

### Kafka Settings

- In `notification_gateway/config/settings/base.py` set `BOOTSTRAP_SERVERS` based on your `kafka-docker` settings.
- In `notification_gateway/local.yml` change the `django` port based on your needs **(optional)**.

## Requests

```python
url: /api/v1/notification-server/notify/

request: {
	"ids": List[int],
	"type": Union["user", "subscription"],
	"provider": Union["mail", "sms", "in_app"],
	"message": {
		"title": String,
		"description": String
	},
	"persist": Boolean,
	"ttl": Union[None, Integer]
}

response: 200
```


## Type checks

Running type checks with mypy:

```sh
  $ mypy notification_gateway
```

## Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report::
```
    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html
```

## Running tests with py.test

```sh
  $ pytest
```
