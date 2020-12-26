"""
Name: Runs a Google Analytics API query
Developer: Matt Clarke
Date: June 8, 2020
Description: Passes a payload to the Google Analytics reporting API and returns the data.
"""

import math
import pandas as pd


def run_query(service, view_id: str, payload: dict, output: str = 'df'):
    """Runs a query against the Google Analytics reporting API and returns the results data.

    :param service: Authenticated Google Analytics service connection
    :param view_id: Google Analytics view ID to query
    :param payload: Payload of query parameters to pass to Google Analytics in Python dictionary
    :param output: String containing the format to return (df or raw)
    Returns data from Google Analytics or an exception message
    """

    required_payload = {'ids': 'ga:' + view_id}
    final_payload = {**required_payload, **payload}

    try:
        results = get_results(service, final_payload)

        if output == 'df':
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


def get_total_results(results):
    """Return the totalResults object from a Google Analytics API request.

    :param results: Google Analytics API results set
    :return: Number of results
    """

    if results['totalResults']:
        return results['totalResults']


def get_items_per_page(results):
    """Return the itemsPerPage object from a Google Analytics API request.

    :param results: Google Analytics API results set
    :return: Number of items per page (default is 1000 if not set, max is 10000)
    """

    if results['itemsPerPage']:
        return results['itemsPerPage']


def get_total_pages(results):
    """Return the total number of pages.

    :param results: Google Analytics API results set
    :return: Number of results
    """

    if results['totalResults']:
        return math.ceil(results['totalResults'] / results['itemsPerPage'])


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
        column_headers = results['columnHeaders']
        headings = []
        for header in column_headers:

            name = header['name'].replace('ga:', '')
            headings.append(name)

        if results['rows']:
            rows = results['rows']

            return pd.DataFrame(rows, columns=headings)


def get_results(service, final_payload):
    """Passes a payload to the API using the service object and returns all available results by merging paginated
    data together into a single DataSet.

    :param service: Google Analytics service object
    :param final_payload: Final payload to pass to API
    :return: Original result object with rows data manipulated to contains rows from all pages
    """

    # Run the query and determine the number of items and pages
    results = service.data().ga().get(**final_payload).execute()
    total_results = get_total_results(results)
    total_pages = get_total_pages(results)
    items_per_page = get_items_per_page(results)

    # Return multiple pages of results
    if total_pages > 1:

        start_index = 0
        all_rows = []

        while start_index <= total_results:

            # Determine start_index and add to payload
            start_index_payload = {'start_index': + start_index + 1}
            final_payload = {**final_payload, **start_index_payload}

            # Fetch results and append rows
            next_results = service.data().ga().get(**final_payload).execute()
            next_rows = get_rows(next_results)
            all_rows = all_rows + next_rows

            # Update start_index
            start_index = (items_per_page + start_index)

        # Replace rows in initial results with all rows
        results['rows'] = all_rows
        return results

    # Return a single page of results
    else:
        return results
