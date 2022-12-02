#Directory for unit tests
import urllib3
import boto3
import aws_cdk as core
import aws_cdk.assertions as assertions
import pytest
import datetime
from aws_cdk import(aws_dynamodb as db_,)
from sprint4.sprint4_stack import Sprint4Stack

# code ref: https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.assertions/Template.html
import requests
import json
import uuid

url = "https://2ukag51771.execute-api.us-east-2.amazonaws.com/prod/URLS"
url_id = str(uuid.uuid4)


def test_http_post_method():

    website = {"url_id": url_id, "url_name": "www.facebook.com"}
    r = requests.post(url, data=json.dumps(website))
    assert r.status_code == 200


def test_http_get_method():
    r = requests.get(url)
    assert r.status_code == 200


def test_http_patch_method():
    website = {"url_id": url_id, "url_name": "www.twitter.com"}
    r = requests.patch(url, data=json.dumps(website))
    assert r.status_code == 200


def test_http_delete_method():
    website = {"url_id": url_id}
    r = requests.delete(url, data=json.dumps(website))
    assert r.status_code == 200