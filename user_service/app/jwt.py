from authlib.jose import RSAKey


def setup_jwk(app):
    app.private_key = RSAKey.generate_key(is_private=True)
    app.public_key = RSAKey.import_key(app.private_key.get_public_key())
