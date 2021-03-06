import json
import uuid

import jwt
from django.conf import settings
from django.db.models import Q
from jwt import InvalidTokenError
from cryptography.hazmat.primitives import serialization
from api.services.KeycloakAPI import map_user

from jwt.algorithms import RSAAlgorithm
from rest_framework import authentication
from rest_framework import exceptions
from api.models.User import User
import requests

from api.models.UserCreationRequest import UserCreationRequest


class UserAuthentication(authentication.BaseAuthentication):

    def _get_keys(self):
        """Assemble a list of valid signing public keys we use to verify the token"""

        decoded_keys = {}

        # We have a test key loaded
        if settings.KEYCLOAK['RS256_KEY'] is not None:
            decoded_keys['imported'] = settings.KEYCLOAK['RS256_KEY']

        if not settings.KEYCLOAK['DOWNLOAD_CERTS']:
            return decoded_keys

        # TODO cache the keys for some amount of time (in the db, perhaps)

        # Download a key directly from Keycloak
        response = requests.get(settings.KEYCLOAK['CERTS_URL'], timeout=5)

        if not response:
            raise RuntimeError('keys not available from {}'.format(settings.KEYCLOAK['CERTS_URL']))

        keys = response.json()
        decoded_keys = {}

        for key in keys['keys']:
            print('key: {}'.format(key))
            if key['alg'] in ['RS256', 'RS384', 'RS512']:
                decoded_keys[key['kid']] = RSAAlgorithm.from_jwk(json.dumps(key)).public_bytes(
                    format=serialization.PublicFormat.SubjectPublicKeyInfo,
                    encoding=serialization.Encoding.PEM).decode('utf-8')

        return decoded_keys

    def authenticate(self, request):
        """Verify the JWT token and find the correct user in the DB"""

        if not settings.KEYCLOAK['ENABLED']:
            # fall through
            return None

        auth = request.META.get('HTTP_AUTHORIZATION', None)

        if not auth:
            raise exceptions.AuthenticationFailed('Authorization header required')

        try:
            scheme, token = auth.split()
        except ValueError:
            raise exceptions.AuthenticationFailed('Invalid format for authorization header')

        if scheme != 'Bearer':
            raise exceptions.AuthenticationFailed(
                'Authorization header invalid'
            )

        if not token:
            raise exceptions.AuthenticationFailed(
                'No token found'
            )

        user_token = None
        token_validation_errors = []

        keys = self._get_keys().items()

        if len(keys) == 0:
            raise exceptions.AuthenticationFailed('no keys available for verification')

        for kid, key in keys:
            try:
                user_token = jwt.decode(token,
                                        key=str(key),
                                        audience=settings.KEYCLOAK['AUDIENCE'],
                                        issuer=settings.KEYCLOAK['ISSUER'])
                break
            except InvalidTokenError as e:
                token_validation_errors.append(e)

        if not user_token:
            raise exceptions.AuthenticationFailed(
                'No successful decode of user token. Exceptions occurred: {}',
                '\n'.join([str(error) for error in token_validation_errors])
            )

        user_found_via_email = None

        if 'user_id' not in user_token:
            # try email
            if 'email' in user_token:
                qs = UserCreationRequest.objects.filter(
                    keycloak_email=user_token['email']
                )

                if not qs.exists():
                    raise exceptions.AuthenticationFailed('user does not exist')

                ucr = qs.first()

                if not ucr.is_mapped:
                    map_user(user_token['sub'], ucr.user.username)

                    ucr.is_mapped = True
                    ucr.save()

                user_found_via_email = ucr.user.username
            else:
                raise exceptions.AuthenticationFailed('user_id or email is required in jwt payload')

        username = user_token['user_id'] if 'user_id' in user_token else user_found_via_email

        try:
            user = User.objects.get_by_natural_key(username)

            if not user.is_active:
                raise exceptions.AuthenticationFailed('user_id "{}" does not exist'.format(username))
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('user_id "{}" does not exist'.format(username))

        return user, None
