from my_app import jwt

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return (
        {"message": "The token has expired.", "error": "token_expired"},
        401,
    )


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        {"message": "Signature verification failed.", "error": "invalid_token"},
        401,
    )


@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        {
            "description": "Request does not contain an access token.",
            "error": "authorization_required",
        },
        401,
    )