from utils import  user_pool_id, parse_cognito_user_dict, cognito_idp_client, region, identity_pool_id,\
    cognito_identity_client, get_response, COGNITO_USER_ID_ATTRIBUTE, get_provider_from_username, de_cloned_error, \
    json, get_formatted_validation_error

from models.auth_model import SocialSignInModel
from pydantic import ValidationError


def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        parsed_body: SocialSignInModel = SocialSignInModel(**body)
        account_id = event['requestContext']['accountId']

        user_response = cognito_idp_client.get_user(
            AccessToken=parsed_body.access_token
        )

        cognito_user = parse_cognito_user_dict(user_response['UserAttributes'])
        login_param = f"cognito-idp.{region}.amazonaws.com/{user_pool_id}"
        id_response = cognito_identity_client.get_id(
            AccountId=account_id,
            IdentityPoolId=identity_pool_id,
            Logins={
                login_param: parsed_body.id_token
            }
        )
        identity_id = id_response['IdentityId']
        resp = cognito_identity_client.get_credentials_for_identity(
            IdentityId=identity_id,
            Logins={
                login_param: parsed_body.id_token
            },
        )
        print("resp", resp)
        
        token_response = {
            "userId": cognito_user.get(COGNITO_USER_ID_ATTRIBUTE),
            "idToken": parsed_body.id_token,
            "accessToken": parsed_body.access_token,
            "refreshToken": parsed_body.refresh_token,
            "expiresIn": parsed_body.expires_in,
            "tokenType": parsed_body.token_type,
            "accessKey": resp['Credentials']['AccessKeyId'],
            "secretKey": resp['Credentials']['SecretKey'],
            "sessionToken": resp['Credentials']['SessionToken'],
            "signInSource": get_provider_from_username(user_response.get("Username", ""))
        }

        return get_response(
            status=200,
            error=False,
            message="Sign in successful",
            data=token_response
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
    except cognito_idp_client.exceptions.NotAuthorizedException as e:
        print(e)
        return get_response(
            status=400,
            error=True,
            code="SIGNIN_NOT_AUTHORIZED",
            message="Incorrect username or password",
        )
    except Exception as e:
        print(e)
        error = str(e)
        if '::PREAUTHENTICATION::' in error:
            code_msg = error.split('::PREAUTHENTICATION::')[1]
            code = msg = code_msg
            if '::CODE::' in code_msg:
                code = code_msg.split('::CODE::')[0]
                msg = code_msg.split('::CODE::')[1]
            
            return get_response(
                status=400,
                error=True,
                code=code,
                message=msg,
            )
        return get_response(
            status=400,
            error=True,
            message=de_cloned_error(str(e)),
        )

