import requests
import json
from typing import Optional
import logging

from models.authentication_options import AuthenticationOptions

class AuthenticationService:
    def __init__(self, options: AuthenticationOptions):
        self._options = options

    def get_access_token(self) -> Optional[str]:
        values = {
            "client_id": self._options.client_id,
            "client_secret": self._options.client_secret,
            "scope": self._options.scope,
            "grant_type": self._options.grant_type,
            "resource": self._options.resource
        }
        request_url = f"{self._options.endpoint}{self._options.tenant_id}/oauth2/token"
        logging.info(request_url)
        logging.info(values)

        try:
            response = requests.post(request_url, data=values)
            response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx
        except requests.RequestException as e:
            print(f"Request to {request_url} failed: {e}")
            return None

        try:
            token_response = response.json()
            logging.info(token_response)
            return token_response.get('access_token')
        except json.JSONDecodeError:
            print("Failed to decode JSON response")
            return None
