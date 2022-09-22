from pydantic import BaseModel, constr


class SocialSignInModel(BaseModel):
    id_token: constr(min_length=3)
    access_token: constr(min_length=3)
    refresh_token: constr(min_length=3)
    expires_in: constr(min_length=3)
    token_type: constr(min_length=3)


class LogoutModel(BaseModel):
    access_token: constr(min_length=3)