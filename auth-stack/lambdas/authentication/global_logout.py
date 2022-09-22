from utils import cognito_idp_client, get_response, de_cloned_error, json, get_formatted_validation_error
from models.auth_model import LogoutModel
from pydantic import ValidationError


def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        parsed_body: LogoutModel = LogoutModel(**body)
        cognito_sign_out_user(parsed_body.access_token)
        return get_response(
            status=200,
            error=False,
            code="USER_LOGGED_OUT",
            message="Logged out",
        )
    except ValidationError as e:
        return get_response(
            status=400,
            error=True,
            code="VALIDATION_ERROR",
            message=get_formatted_validation_error(e),
        )
    except cognito_idp_client.exceptions.UserNotFoundException as e:
        print(e)
        return get_response(
            status=400,
            error=True,
            code="USER_NOT_FOUND",
            message="No user found with provided email/phone!",
        )
    except cognito_idp_client.exceptions.UserNotConfirmedException as e:
        print(e)
        return get_response(
            status=400,
            error=True,
            code="USER_NOT_CONFIRMED",
            message="User account not confirmed! Check email/sms for account confirmation code",
        )
    except cognito_idp_client.exceptions.TooManyRequestsException as e:
        print(e)
        return get_response(
            status=400,
            error=True,
            code="TOO_MANY_REQUESTS",
            message="Request limit exceeded! Please retry after a short while",
        )
    except Exception as e:
        print(e)
        return get_response(
            status=400,
            error=True,
            message=de_cloned_error(str(e)),
        )


def cognito_sign_out_user(access_token):
    sign_out_user_response = cognito_idp_client.global_sign_out(
        AccessToken=access_token
    )
    return sign_out_user_response
