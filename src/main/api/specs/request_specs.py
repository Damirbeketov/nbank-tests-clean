import requests
import logging

from src.main.api.configs.config import Config


class RequestSpecs:
    @staticmethod
    def default_req_headers():
        return {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    @staticmethod
    def unauth_spec():
        return {
            "base_url": f"{Config.get('server')}{Config.get('api_version')}",
            "headers": RequestSpecs.default_req_headers()
        }

    @staticmethod
    def admin_auth_spec():
        headers = RequestSpecs.default_req_headers()
        headers["Authorization"] = Config.get("ADMIN_AUTH_HEADER", "Basic YWRtaW46YWRtaW4=")
        return {
            "base_url": f"{Config.get('server')}{Config.get('api_version')}",
            "headers": headers
        }

    @staticmethod
    def auth_as_user(username, password):
        login_url = f"{Config.get('server')}{Config.get('api_version')}/auth/login"
        response = requests.post(login_url, json={"username": username, "password": password})

        if response.status_code == 200:
            auth_header = response.headers.get("Authorization")
            headers = RequestSpecs.default_req_headers()
            headers["Authorization"] = auth_header
            return {
                "base_url": f"{Config.get('server')}{Config.get('api_version')}",
                "headers": headers
            }
        else:
            logging.error(f"Authentication failed for {username}")
            raise Exception("Failed to authenticate user")