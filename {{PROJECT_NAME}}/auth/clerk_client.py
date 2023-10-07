# Object used for interacting with the Clerk API

import requests
import json
import jwt
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass
from flask import g, current_app

@dataclass
class ClerkUser:
    id: str
    email: str


class ClerkClient:
    users_url = "/users"
    sessions_url = "/sessions"

    jwt_instance = jwt.JWT()

    def __init__(self, api_key, logger: logging.Logger = None):
        self.api_key = api_key
        self.base_url = "https://api.clerk.dev/v1"

        self.logger = logger
        if self.logger is None:
            self.logger = logging.getLogger(__name__)


    def __get_headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def __get_user(self, user_id: str) -> Optional[ClerkUser]:
        url = f"{self.base_url}{self.users_url}/{user_id}"

        response = requests.get(url, headers=self.__get_headers())

        try:
            response_body: Dict[str, Any] = response.json()
        except json.JSONDecodeError as e:
            self.logger.error(f"failed to decode response: {response.text}")
            return None

        if response.status_code != 200:
            self.logger.error(f"invalid user id: {user_id} {response.status_code}")
            for errors in response_body.get("errors", []):
                self.logger.error(f"error: {errors.get('long_message', 'unknown error')}") 
            return None
        
        # get the email from the response
        primary_email_id = response_body.get("primary_email_address_id", None)

        if primary_email_id is None:
            self.logger.error(f"invalid user id: {user_id} no primary email")
            return None

        primary_email = None
        for email in response_body.get("email_addresses", []):
            if email.get("id", None) == primary_email_id:
                primary_email = email.get("email_address", None)
                break
        
        if primary_email is None:
            self.logger.error(f"invalid user id: {user_id} no primary email")
            return None

        return ClerkUser(
            id=user_id,
            email=primary_email
        )

    
    def verify_session(self, session_token:str) -> Optional[ClerkUser]:
        # parse the token with jwt
        try:
            # no need to verify the token because we are going to check it with clerk
            claims = self.jwt_instance.decode(session_token, do_verify=False, do_time_check=True)

            if claims is None:
                raise jwt.exceptions.JWTError("no claims")
        except jwt.exceptions.JWTException as e:
            self.logger.error(f"jwt failed to decode: {e}")
            return None
        except Exception as e:
            self.logger.error(f"failed to decode response: {e}")
            return None

        current_app.logger.debug(f"claims: {claims}")
        
        session_id = claims.get("sid", None)
        user_id = claims.get("sub", None)

        # if the session id or user id is missing, the token is invalid
        if session_id is None or user_id is None:
            self.logger.error(f"jwt missing session id or user id: {session_token}")
            return None

        # make a request to the sessions endpoint
        url = f"{self.base_url}{self.sessions_url}/{session_id}/verify"
        body = {
            "token": session_token
        }

        response = requests.post(url, headers=self.__get_headers(), data=json.dumps(body))

        try:
            response_body: Dict[str, Any] = response.json()
        except json.JSONDecodeError as e:
            self.logger.error(f"failed to decode response: {response.text}")
            return None

        current_app.logger.debug(f"response: {response_body}")

        # if the response is not 200, the token is invalid
        if response.status_code != 200:
            self.logger.error(f"invalid session token: {session_token} {response.status_code}")
            for errors in response_body.get("errors", []):
                self.logger.error(f"error: {errors.get('long_message', 'unknown error')}") 
            return None

        # check if the session is active
        if response_body.get("status", "") != "active":
            self.logger.error(f"invalid session token: {session_token} session not active")
            return None

        # if the user id in the response does not match the user id in the token, the token is invalid
        if response_body.get("user_id", "") != user_id:
            self.logger.error(f"invalid session token: {session_token} user id mismatch")
            return None

        # make a request to the users endpoint
        return self.__get_user(user_id)

def get_client() -> ClerkClient:
    if "clerk_client" not in g:
        g.clerk_client = ClerkClient(
            api_key=current_app.config["CLERK_BACKEND_KEY"],
            logger=current_app.logger
        )

    return g.clerk_client
