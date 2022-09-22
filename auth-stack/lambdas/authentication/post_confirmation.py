# from auth_utils import email_phone_exists, add_user_to_group, add_aurora_user, add_dynamo_user
# from global_utils import connection, cognito_idp_client, add_msg_to_sqs, get_sqs_email_msg
# from model_dataclass.auth_model import SignupModel, UserModel
# from model_dataclass.constants import INITIAL_ROLE, EMAIL_MEDIUM, COGNITO_EXTERNAL_SIGNUP_MEDIUM_VALUE, \
#     COGNITO_SIGNUP_MEDIUM_ATTRIBUTE, COGNITO_USER_ID_ATTRIBUTE


def lambda_handler(event, context):
    print(event)
    shouldCommit = False
    try:

        return event

    except Exception as error:
        print(error)
        raise Exception(f"::POSTCONFIRMATION::{str(error)}")
