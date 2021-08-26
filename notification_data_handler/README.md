# Notification Data Handler Service

This service exposes the APIs to fetch user and subscription details and also provides facilities to subscribe users to topics.

## Settings

### Django Settings
- In `notification_data_handler/local.yml` change the django port based on your needs **(optional)**.

## Basic Commands

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create an **superuser account**, use this command::
```sh
    $ python manage.py createsuperuser
```
For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

## Type checks

Running type checks with mypy:
```sh
  $ mypy notification_data_handler
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


## Requests

### Users

- `GET` user details.

```python
url: /api/v1/users/get-user-details/<int:id>/

request: 
    url params: id

response: {
    "id": 1,
    "name": "ABC",
    "first_name": null,
    "last_name": null,
    "email": "abc@xyz.com",
    "phone": null,
    "device": [
        {
            "device_type": "Mobile",
            "device_id": "678953YUB4532"
        }
    ]
}
```

### Subscription

- `GET` subscription details.

```python
url: /api/v1/subscription/get-subscribed-users/<int:id>/

request: 
    url params: id

response: {
    "id": 1,
    "user": [
        {
            "id": 1,
            "name": "ABC",
            "first_name": null,
            "last_name": null,
            "email": "abc@xyz.com",
            "phone": null,
            "device": [
                {
                    "device_type": "Mobile",
                    "device_id": "678953YUB4532"
                }
            ]
        }
    ],
    "topic": "Discount",
    "created": "2021-08-23T16:50:57.189636Z",
    "modified": "2021-08-23T16:50:57.189636Z",
    "is_active": true,
    "is_deleted": false,
    "name": "Discount"
}
```

- `POST` create subscription.

```python
url: /api/v1/subscription/create-subscription/

request: {
	"name": "abc",
	"user": [1, 2, 3],
	"topic": 1
}

response: 201
```

- `PUT/PATCH` update subscription.

```python
url: /api/v1/subscription/update-subscription/

request: {
	"name": "xyz",
	"user": [1, 2],
	"topic": 1
}

response: 200
```

- `GET` List subscription.

```python
url: /api/v1/subscription/list-subscription/


response: [{
	"name": "xyz",
	"user": [1, 2],
	"topic": 1
}]
```

