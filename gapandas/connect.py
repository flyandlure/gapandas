"""
Name: Connect to the Google Analytics API
Developer: Matt Clarke
Date: June 8, 2020
Description: Authenticates with the Google Analytics API using a client secrets JSON key file
and returns a Google Analytics service for use in other functions.
"""

import socket
import sys
import os.path
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

# Prevent "The read operation timed out" errors
socket.setdefaulttimeout(500)


def get_service(keyfile_path, verbose=False):
    """Return a service to communicate with the Google Analytics API
       using settings from the configuration file.

    :param keyfile_path - Path to client_secrets.json
    :param verbose: Set to True to see messages
    """

    if verbose:
        print('Attempting connection')

    if not os.path.exists(keyfile_path):
        print('Keyfile not found')
        sys.exit()

    else:

        try:
            credentials = ServiceAccountCredentials.from_json_keyfile_name(keyfile_path,
                                                                           scopes="https://www.googleapis.com/auth"
                                                                                  "/analytics.readonly")
            service = build("analytics", "v3", credentials=credentials)

            if verbose:
                print('Connected successfully')

            return service

        except Exception as e:

            if verbose:
                print('Connection failed: \
                Ensure your keyfile is correct and you have added the email to your Google Analytics account.')

            return e
