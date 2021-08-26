# Provider Handler Service

This service provides functionalities like fetching from queue (here kafka) and assigning notification to respective providers for processing notification to users.


## Settings

### Kafka Settings

- In `notification_validator/config/settings/base.py` set `BOOTSTRAP_SERVERS_CONSUMER` based on your kafka-docker settings.

### Django Settings

- In `notification_validator/local.yml` change the django port based on your needs (optional).


## Type checks

Running type checks with mypy:
```sh
  $ mypy notification_validator
```

## Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report::
```sh
    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html
```

## Running tests with py.test
```sh
  $ pytest
```

## Celery

This app comes with Celery.

To run a celery worker:

```sh
    $ cd notification_validator
    $ celery -A config.celery_app worker -l info
```

Please note: For Celery's import magic to work, it is important *where* the celery commands are run. If you are in the same folder with *manage.py*, you should be right.

*You can set the providers here as per your requirements*
