"""
Name: Runs a Google Analytics API query
Developer: Matt Clarke
Date: June 8, 2020
Description: Passes a payload to the Google Analytics reporting API and returns the data.
"""

import pandas as pd


def run_query(service, view_id: str, payload: dict, format: str = 'df'):
    """Runs a query against the Google Analytics reporting API and returns the results data.

    :param service: Authenticated Google Analytics service connection
    :param view_id: Google Analytics view ID to query
    :param payload: Payload of query parameters to pass to Google Analytics in Python dictionary
    :param format: String containing the format to return (df or raw)
    Returns data from Google Analytics or an exception message
    """

    required_payload = {'ids': 'ga:' + view_id}
    final_payload = {**required_payload, **payload}
    try:
        results = service.data().ga().get(**final_payload).execute()

        if format == 'df':
            return results_to_pandas(results)
        else:
            return results

    except Exception as e:
        return e


def get_profile_info(results):
    """Return the profileInfo object from a Google Analytics API request. This contains various parameters, including
    the profile ID, the query parameters, the link used in the API call, the number of results and the pagination.

    :param results: Google Analytics API results set
    :return: Python dictionary containing profileInfo data
    """

    if results['profileInfo']:
        return results['profileInfo']


def get_totals(results):
    """Return the totalsForAllResults object from a Google Analytics API request.

    :param results: Google Analytics API results set
    :return: Python dictionary containing totalsForAllResults data
    """

    if results['totalsForAllResults']:
        return results['totalsForAllResults']


def get_rows(results):
    """Return the rows object from a Google Analytics API request.

    :param results: Google Analytics API results set
    :return: Python dictionary containing rows data
    """

    if results['rows']:
        return results['rows']


def get_column_headers(results):
    """Return the columnHeaders object from a Google Analytics API request.

    :param results: Google Analytics API results set
    :return: Python dictionary containing columnHeaders data
    """

    if results['columnHeaders']:
        return results['columnHeaders']


def results_to_pandas(results):
    """Return a Google Analytics result set in a Pandas DataFrame.

    :param results: Google Analytics API results set
    :return: Pandas DataFrame containing results
    """

    if results['columnHeaders']:
        columnHeaders = results['columnHeaders']
        headings = []
        for header in columnHeaders:

            name = header['name'].replace('ga:', '')
            headings.append(name)

        if results['rows']:
            rows = results['rows']

            return pd.DataFrame(rows, columns=headings)

