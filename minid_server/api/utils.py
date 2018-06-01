from app import app

try:
    import globus_sdk
    GLOBUS_AUTH_ENABLED = bool(app.config.get('GLOBUS_CLIENT_ID') and
                               app.config.get('GLOBUS_CLIENT_SECRET'))
except ImportError:
    GLOBUS_AUTH_ENABLED = False


def validate_globus_user(email, authorization_header):

    scheme, token = authorization_header.split()
    if str(scheme) != 'Bearer':
        raise AuthorizationException('Only Bearer token scheme is supported '
                                     'for Globus Auth',
                                     user=email, type='InvalidToken')
    client = globus_sdk.ConfidentialAppAuthClient(
        app.config.get('GLOBUS_CLIENT_ID'),
        app.config.get('GLOBUS_CLIENT_SECRET')
    )
    info = client.oauth2_token_introspect(token, 'identity_set')
    if info.data.get('active') is False:
        raise AuthorizationException('Expired or invalid Globus Auth '
                                     'code.', user=email,
                                     type='AuthorizationFailed')
    ids = client.get_identities(ids=info.data['identity_set'])
    linked_emails = [str(u_id['username'])
                     for u_id in ids['identities']]
    if email not in linked_emails:
        # We're assuming the user just needs to link their id. It's
        # possible they're an impersonator and we should raise an error
        raise AuthorizationException('User needs to link their email '
                                     '%s to their Globus identity: '
                                     'globus.org/app/account' % email,
                                     user=email,
                                     type='InvalidIdentity')


class AuthorizationException(Exception):
    def __init__(self, message, errors=None, user=None, code=401,
                 type='AuthorizationFailed'):
        super(AuthorizationException, self).__init__(message)
        self.message = message
        self.user = user
        self.code = code
        self.type = type
