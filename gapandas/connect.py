"""
Name: Connect to the Google Analytics API
Developer: Matt Clarke
Date: June 8, 2020
Description: Authenticates with the Google Analytics API using a client secrets JSON key file
and returns a Google Analytics service for use in other functions.
"""

from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


def get_service(keyfile_path):
    """Return a service to communicate with the Google Analytics API
       using settings from the configuration file.

    :param keyfile_path - Path to client_secrets.json
    """

    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(keyfile_path,
                                                                       scopes="https://www.googleapis.com/auth/analytics.readonly")
        service = build("analytics", "v3", credentials=credentials)
        return service

    except Exception as e:
        return e
