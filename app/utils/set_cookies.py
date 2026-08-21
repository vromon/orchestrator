from fastapi import Response
def set_cookies(response:Response,access_token,refresh_token):

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        max_age=60

    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        max_age=30*24*3600

    )  