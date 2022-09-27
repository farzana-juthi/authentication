# from global_utils import get_db_user
# from model_dataclass.constants import COGNITO_USER_ID_ATTRIBUTE
# from auth_utils import is_user_blocked


def lambda_handler(event, context):
    print(event)

    try:
        return event
    except Exception as error:
        raise Exception(f"::PREAUTHENTICATION::{str(error)}")


