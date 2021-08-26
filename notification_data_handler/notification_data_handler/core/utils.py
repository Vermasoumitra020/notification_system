# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

# python imports
import math
import os
import re
import pytz
import requests
import json
from random import choice, SystemRandom
from string import digits, ascii_uppercase, ascii_lowercase

# third party imports
import logging
import jwt
import base64
# imports from the crypto libs
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers

# django imports
from django import template
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.utils.text import slugify
from django.utils import timezone
from django.conf import settings
from datetime import timedelta, datetime


# logger implementations
logger = logging.getLogger()

import environ



def optimized_queryset(self, request):
    fields = self.__class__.model._meta.get_fields()
    fks = [field.name for field in fields if field.many_to_one and field.concrete]
    m2m = [field.name for field in fields if field.many_to_many and field.concrete]
    return (
        super(self.__class__, self)
            .get_queryset(request)
            .select_related(*fks)
            .prefetch_related(*m2m)
    )


def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""

    def in_groups(u):
        if u.is_authenticated():
            if u.is_superuser | bool(u.groups.filter(name__in=group_names)):
                return True
        return False

    return user_passes_test(in_groups, login_url="/dashboard/activate/")


def profile_pic_location(instance, filename):
    model = str(instance.__class__.__name__).lower()
    if model == "userprofile":
        return "%s/%s" % ("userprofile", filename)
    return


def generate_random_string(length=5):
    digit_len = length // 2
    alpha_len = length - digit_len
    return "".join(
        [choice(digits) for _ in range(digit_len)]
        + [choice(ascii_lowercase) for _ in range(alpha_len)]
    )


# instance_class because import dependency will get fucked if import from qna
# behaviours is importing utils, mixins are in behaviours which are used in models hence can not import models in utils
def create_slug(instance, new_slug=None, append_string=None):
    if new_slug is not None:
        slug = new_slug
    elif instance.slug:
        slug = instance.slug
    elif hasattr(instance, "title"):
        slug = slugify(instance.title)
    elif hasattr(instance, "name"):
        slug = slugify(instance.name)
    else:
        slug = None
    if append_string and slug:
        slug = slugify(append_string + slug)
    if slug:
        qs = instance.__class__.objects.filter(slug=slug).order_by("-id")
        exists = True if qs.exists() and qs.first().id != instance.id else False
        if exists:
            # print qs
            # print "old_slug",slug
            new_slug = "%s-%s" % (slug, generate_random_string(length=5))
            # print "new_slug",new_slug
            return create_slug(instance, new_slug=new_slug)
        if len(slug) > 50:
            slug = slug[:44] + "-" + generate_random_string(length=5)
        if not slug:
            slug = generate_random_string(length=5)
        return slug
    else:
        return None


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        """Returns a filename that's free on the target storage system, and
        available for new content to be written to.

        Found at http://djangosnippets.org/snippets/976/

        This file storage solves overwrite on upload problem. Another
        proposed solution was to override the save method on the model
        like so (from https://code.djangoproject.com/ticket/11663):

        def save(self, *args, **kwargs):
            try:
                this = MyModelName.objects.get(id=self.id)
                if this.MyImageFieldName != self.MyImageFieldName:
                    this.MyImageFieldName.delete()
            except: pass
            super(MyModelName, self).save(*args, **kwargs)
        """
        # If the filename already exists, remove it as if it was a true file system
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name



def validate_mobile(mobile):
    if re.match(r"^[789]\d{9}$", mobile):
        return True
    else:
        return False


def split_full_name(name):
    name_set = name.strip().split(" ")
    first_name = name_set[0]
    last_name = " ".join(name_set[1:])
    # index = 0
    # for nm in name_set:
    #     if index != 0:
    #         last_name = last_name + " " + nm
    #     index += 1
    return [first_name, last_name]


def generate_smart_id(length=10):
    """
    Generates a random alphanumeric string used as an ID.
    """
    return "".join(
        SystemRandom().choice(ascii_uppercase + digits) for _ in range(length)
    )


def clean_string(string):
    """
    Clean an input string by removing all non unicode characters
    :param string: input string
    :return: string by removing all non unicode characters
    """
    return string.decode("ascii", errors="ignore")


register = template.Library()


@register.filter
def truncate_text(value, limit=80):
    """
    Truncates a string after a given number of chars keeping whole words.

    Usage:
        {{ string|truncatesmart }}
        {{ string|truncatesmart:50 }}
    """

    try:
        limit = int(limit)
    # invalid literal for int()
    except ValueError:
        # Fail silently.
        return value

    # Make sure it's unicode
    value = str(value)

    # Return the string itself if length is smaller or equal to the limit
    if len(value) <= limit:
        return value

    # Cut the string
    value = value[:limit]

    # Break into words and remove the last
    words = value.split(" ")[:-1]

    # Join the words and return
    return " ".join(words) + "..."


def get_user_agent(http_agent):
    print(http_agent)
    if re.match(r".*(mobile|android|iphone|ipad|tablet).*", http_agent, re.IGNORECASE):
        return "mobile"
    return "desktop"






# Authentication and authorization functions
# ---------------------------------------------------------------------------------------------------------------------


# class InvalidAuthorizationToken(Exception):
#     """
#     class to handle token decode exceptions
#     """
#
#     def __init__(self, details):
#         self.super().__init__("Invalid authorization token: " + details)
#
#
# def ensure_bytes(key):
#     """
#     ENABLER
#     :param key:
#     :return: key
#     """
#     if isinstance(key, str):
#         key = key.encode("utf-8")
#     return key
#
#
# def decode_value(val):
#     """
#     ENABLER
#     :param val:
#     :return:
#     """
#     decoded = base64.urlsafe_b64decode(ensure_bytes(val) + b"==")
#     return int.from_bytes(decoded, "big")
#
#
# def generate_public_key(json_web_key):
#     """
#     METHOD NAME         :   generate_public_key
#     DESCRIPTION         :   generates public certificate to decode
#     PARAMETERS          :   jwk(json web key)
#     RETURN              :   returns public cert
#     """
#     return (
#         RSAPublicNumbers(
#             n=decode_value(json_web_key["n"]), e=decode_value(json_web_key["e"])
#         )
#             .public_key(default_backend())
#             .public_bytes(
#             encoding=serialization.Encoding.PEM,
#             format=serialization.PublicFormat.SubjectPublicKeyInfo,
#         )
#     )
#
#
# def get_key_id(token):
#     """
#     METHOD NAME         :   get_key_id
#     DESCRIPTION         :   checks for the key id from header of jwt
#     PARAMETERS          :   jwt token
#     RETURN              :   returns key_id (key id)
#     EXCEPTION           :   missing Key_id custom exception
#     """
#     headers = jwt.get_unverified_header(token)
#     if not headers:
#         raise InvalidAuthorizationToken("missing headers")
#     try:
#         return headers["kid"]
#     except KeyError:
#         raise InvalidAuthorizationToken("missing key id")
#
#
# def get_jwk(key_id):
#     """
#     METHOD NAME         :   get_jwk
#     DESCRIPTION         :   dynamically fetches the jwt keys from microsoft's discovery/keys endpoints
#                             and matches
#     PARAMETERS          :   kid(key id)
#     RETURN              :   returns kid
#     EXCEPTION           :   Kid(key id) not Matched exception
#         """
#     method = "GET"
#     headers = {"Accept": "application/json", "cache-control": "no-cache"}
#     logger.info(
#         "requesting Microsoft for keys https://login.microsoftonline.com/TENANT_ID/discovery/keys"
#     )
#     json_web_keys = requests.request(method, AZURE_KEYS_URLS, headers=headers).json()
#
#     for json_web_key in json_web_keys.get("keys"):
#         if json_web_key.get("kid") == key_id:
#             return json_web_key
#     raise InvalidAuthorizationToken("key id not recognized")
#
#
# def get_public_key(token):
#     """
#     ENABLER
#     :param token:
#     :return:
#     """
#     return generate_public_key(get_jwk(get_key_id(token)))
#
#
# def validate_jwt(jwt_to_validate, is_graph):
#     """
#     METHOD NAME         :   validate_jwt
#     DESCRIPTION         :   decodes and verifies id_token with azure's public key
#     PARAMETERS          :   jwk(json web key)
#     RETURN              :   user_context
#     """
#     try:
#         if is_graph:
#             audience = AUDIENCE[0]
#             issuer = ISSUER[0]
#         else:
#             audience = AUDIENCE[0]
#             issuer = ISSUER[0]
#         public_key = get_public_key(jwt_to_validate)
#         print(public_key)
#         decoded = jwt.decode(
#             jwt_to_validate,
#             public_key,
#             verify=0,
#             algorithms=["RS256"],
#             audience=audience,
#             issuer=issuer,
#         )
#         logger.info("DECODED JWT WITH [RS256] Algorithm")
#
#         if is_graph:
#             logger.info("User " + decoded["preferred_username"] + " is requesting")
#             if decoded.get("roles") is None:
#                 context = {"status": False, "message": "USER HAS NO ROLES ASSIGNED"}
#                 logger.error("NO ROLE ATTRIBUTE IN THE USER TOKEN")
#                 return context
#
#             logger.info(decoded["roles"])
#             context = {
#                 "roles": decoded["roles"],
#                 "user": decoded["preferred_username"],
#                 "is_graph": True,
#                 "status": True,
#             }
#         else:
#             logging.info("application " + decoded["appid"])
#             context = {"status": True, "is_graph": True, "app_id": decoded["appid"]}
#         return context
#
#     except Exception as e:
#         logger.error("following error occurred while parsing JWT [" + str(e) + "]")
#         context = {
#             "status": False,
#             "message": "NOT ABLE TO VERIFY REQUEST, CHECK TOKEN",
#         }
#         return context
#
#
# def decode_jwt(token, is_graph):
#     """
#     METHOD NAME         :   decode_jwt
#     DESCRIPTION         :   decodes ad signed jwt
#     PARAMETERS          :   token
#     RETURN              :   object (json)
#     EXCEPTION           :   200 after function executed
#     """
#     try:
#         return validate_jwt(token, is_graph)
#     except Exception as e:
#         logger.error(str(e))
#         return {"error": "Internal server error"}
#
#
# def admin_bypass(request_path):
#     """
#     This func bypasses middleware for admin requests
#     :param request_path:
#     :return:
#     """
#     if request_path.split("/")[1] == ADMIN_URL.split("/")[0]:
#         logger.info("Admin Request")
#         return True
#     else:
#         return False
#
#
# def is_azure_login(request_path):
#     """
#     This func bypasses middleware for admin requests
#     :param request_path:
#     :return:
#     """
#     print(request_path)
#     if request_path == '/app/':
#         logger.info("Admin Request")
#         return True
#     else:
#         return False
#
#
# def is_session_login(request):
#     print(request.META)
#     if request.user.is_authenticated:
#         if len(request.user.password) > 0:
#             return True
#


#
# def get_daemon_token():
#     app = msal.ConfidentialClientApplication(
#         CLIENT_ID, authority=GRANT_TYPE,
#         client_credential=CLIENT_SECRET)
#
#     result = None
#     result = app.acquire_token_silent(SCOPE, account=None)
#
#     if not result:
#         result = app.acquire_token_for_client(scopes=SCOPE)
#
#     if "access_token" not in result:
#         pass
#         # logger.warning("No access token generated")
#
#     else:
#         logger.info("Access token generated")
#
#     header = create_header(result['access_token'])
#     return header


# def create_header(token):
#     """
#     METHOD NAME         :   create_header
#     DESCRIPTION         :   creates header
#     PARAMETERS          :   http request object
#     RETURN              :   object (json)
#     """
#     print(token)
#     return {"Authorization": token, "cache-control": "no-cache"}















