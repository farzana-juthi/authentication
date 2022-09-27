import boto3
import os
import json
import decimal
from datetime import date

region = os.environ.get('AWS_REGION', None)
cognito_idp_client = boto3.client('cognito-idp')
user_pool_id = os.environ.get('USER_POOL_ID', None)
identity_pool_id = os.environ.get('IDENTITY_POOL_ID', None)
cognito_identity_client = boto3.client('cognito-identity')

COGNITO_USER_ID_ATTRIBUTE = 'custom:customUserId'


def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        # should float be used? rounding, precision issues
        # return float(obj)
        return str(obj)
    if isinstance(obj, date):
        return str(obj)
    raise TypeError


def parse_cognito_user_dict(attributes):
    cognito_user = {}
    for item in attributes:
        cognito_user[item['Name']] = item['Value']
    return cognito_user


def get_provider_from_username(username):
    if username.startswith('Facebook_'):
        return 'FACEBOOK'
    return 'REGULAR'


def get_response(status=400, error=True, code="GENERIC", message="Failed to operate", data={}, headers={}):
    default_headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "*",
        "Access-Control-Allow-Headers": "*",
    }
    final_headers = {**default_headers, **headers}
    return {
        "statusCode": status,
        "headers": final_headers,
        "body": json.dumps({
            "error": error,
            "code": code,
            "message": message,
            "data": data
        }, default=decimal_default),
    }


def de_cloned_error(error):
    if ":" in error:
        error = error.split(":")[1].strip()
    return error


def get_formatted_validation_error(e):
    errors = []
    for err in e.errors():
        errors.append(f"{err['loc'][0]}: {err['msg']}")

    return ','.join(errors)
