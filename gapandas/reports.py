"""
Name: A selection of commonly used reports
Developer: Matt Clarke
Date: April 15, 2021
"""

import pandas as pd
from gapandas import connect
from gapandas import query


def monthly_ecommerce_overview(service, view, start_date, end_date, segment=None, filters=None, format=True):
    """Return a dataframe of common ecommerce metrics grouped by year and month.

    Args:
        service (object): Google Analytics API service object.
        view (string): Google Analytics view ID.
        start_date (string): Start date in YYYY-MM-DD format.
        end_date (string): Start date in YYYY-MM-DD format.
        segment (string, optional): Optional Google Analytics segment to apply.
        filters (string, optional): Optional Google Analytics filters to apply.
        format (bool, optional): Set to False to return numeric data, or True to add % and £ where relevant
    Returns:
        df (dataframe): Pandas dataframe of results.

    """

    api_payload = {
        'start_date': start_date,
        'end_date': end_date,
        'metrics': 'ga:entrances, ga:sessions, ga:pageviews, ga:transactions, \
    ga:transactionsPerSession, ga:transactionRevenue, ga:revenuePerTransaction',
        'dimensions': 'ga:yearMonth',
        'sort': '-ga:yearMonth'
    }

    if segment:
        api_payload['segment'] = segment

    if filters:
        api_payload['filters'] = filters

    df = query.run_query(service, view, api_payload)

    df['date'] = pd.to_datetime(df['yearMonth'], format='%Y%m')
    df['yearMonth'] = df['date'].dt.strftime('%B, %Y')
    df = df.drop(columns=['date'])
    df = df.rename(columns={
        'yearMonth': 'Period',
        'entrances': 'Entrances',
        'sessions': 'Sessions',
        'pageviews': 'Pageviews',
        'transactions': 'Transactions',
        'transactionsPerSession': 'Conversion rate',
        'revenuePerTransaction': 'AOV',
        'transactionRevenue': 'Revenue',
    })

    if format:
        df['Entrances'] = df['Entrances'].map('{:,.0f}'.format)
        df['Sessions'] = df['Sessions'].map('{:,.0f}'.format)
        df['Pageviews'] = df['Pageviews'].map('{:,.0f}'.format)
        df['Transactions'] = df['Transactions'].map('{:,.0f}'.format)
        df['Conversion rate'] = df['Conversion rate'].map('{:,.2f}%'.format)
        df['AOV'] = df['AOV'].map('£{:,.2f}'.format)
        df['Revenue'] = df['Revenue'].map('£{:,.0f}'.format)

    return df


def monthly_coupons_overview(service, view, start_date, end_date, format=True):
    """Return a dataframe of common coupon metrics grouped by year and month.

    Args:
        service (object): Google Analytics API service object.
        view (string): Google Analytics view ID.
        start_date (string): Start date in YYYY-MM-DD format.
        end_date (string): Start date in YYYY-MM-DD format.
        segment (string, optional): Optional Google Analytics segment to apply.
        filters (string, optional): Optional Google Analytics filters to apply.
        format (bool, optional): Set to False to return numeric data, or True to add % and £ where relevant

    Returns:
        df (dataframe): Pandas dataframe of results.

    """

    # All orders
    api_payload = {
        'start_date': start_date,
        'end_date': end_date,
        'metrics': 'ga:transactions, ga:transactionRevenue, ga:revenuePerTransaction',
        'dimensions': 'ga:yearMonth',
        'sort': '-ga:yearMonth'
    }

    df_all_orders = query.run_query(service, view, api_payload)
    df_all_orders['date'] = pd.to_datetime(df_all_orders['yearMonth'], format='%Y%m')
    df_all_orders['yearMonth'] = df_all_orders['date'].dt.strftime('%B, %Y')
    df_all_orders = df_all_orders.drop(columns=['date'])
    df_all_orders = df_all_orders.rename(columns={
        'yearMonth': 'Period',
        'transactions': 'Transactions',
        'revenuePerTransaction': 'AOV',
        'transactionRevenue': 'Revenue',
    })

    # Coupon orders
    api_payload = {
        'start_date': start_date,
        'end_date': end_date,
        'metrics': 'ga:transactions, ga:transactionRevenue, ga:revenuePerTransaction',
        'dimensions': 'ga:yearMonth',
        'sort': '-ga:yearMonth',
        'filters': 'ga:orderCouponCode!=(not set)'
    }

    df_coupon = query.run_query(service, view, api_payload)
    df_coupon['date'] = pd.to_datetime(df_coupon['yearMonth'], format='%Y%m')
    df_coupon['yearMonth'] = df_coupon['date'].dt.strftime('%B, %Y')
    df_coupon = df_coupon.drop(columns=['date'])
    df_coupon = df_coupon.rename(columns={
        'yearMonth': 'Period',
        'transactions': 'Coupon transactions',
        'revenuePerTransaction': 'Coupon AOV',
        'transactionRevenue': 'Coupon revenue',
    })

    # Non-coupon
    api_payload = {
        'start_date': start_date,
        'end_date': end_date,
        'metrics': 'ga:transactions, ga:transactionRevenue, ga:revenuePerTransaction',
        'dimensions': 'ga:yearMonth',
        'sort': '-ga:yearMonth',
        'filters': 'ga:orderCouponCode==(not set)'
    }

    df_non_coupon = query.run_query(service, view, api_payload)
    df_non_coupon['date'] = pd.to_datetime(df_non_coupon['yearMonth'], format='%Y%m')
    df_non_coupon['yearMonth'] = df_non_coupon['date'].dt.strftime('%B, %Y')
    df_non_coupon = df_non_coupon.drop(columns=['date'])
    df_non_coupon = df_non_coupon.rename(columns={
        'yearMonth': 'Period',
        'transactions': 'Non-coupon transactions',
        'revenuePerTransaction': 'Non-coupon AOV',
        'transactionRevenue': 'Non-coupon revenue',
    })

    # Merge data
    df_all = df_coupon.merge(df_non_coupon, on='Period', how='left')
    df_all = df_all.merge(df_all_orders, on='Period', how='left')

    # Calculate metrics
    df_all['Coupon AOV uplift'] = round(df_all['Coupon AOV'] - df_all['AOV'], 2)
    df_all['Transactions via coupons'] = round((df_all['Coupon transactions'] / df_all['Transactions']) * 100, 2)
    df_all['Revenue via coupons'] = round((df_all['Coupon revenue'] / df_all['Revenue']) * 100, 0)

    # Reformat data
    df_all = df_all[
        ['Period', 'Coupon transactions', 'Transactions via coupons', 'Coupon revenue', 'Revenue via coupons',
         'Coupon AOV', 'Non-coupon AOV', 'Coupon AOV uplift']]

    if format:
        df_all['Coupon transactions'] = df_all['Coupon transactions'].map('{:,.0f}'.format)
        df_all['Transactions via coupons'] = df_all['Transactions via coupons'].map('{:,.2f}%'.format)
        df_all['Coupon revenue'] = df_all['Coupon revenue'].map('£{:,.0f}'.format)
        df_all['Revenue via coupons'] = df_all['Revenue via coupons'].map('{:,.2f}%'.format)
        df_all['Coupon AOV'] = df_all['Coupon AOV'].map('£{:,.2f}'.format)
        df_all['Non-coupon AOV'] = df_all['Non-coupon AOV'].map('£{:,.2f}'.format)
        df_all['Coupon AOV uplift'] = df_all['Coupon AOV uplift'].map('£{:,.2f}'.format)

    return df_all


def monthly_google_ads_overview(service, view, start_date, end_date, format=True):
    """Return a dataframe of common Google Ads grouped by year and month.

    Args:
        service (object): Google Analytics API service object.
        view (string): Google Analytics view ID.
        start_date (string): Start date in YYYY-MM-DD format.
        end_date (string): Start date in YYYY-MM-DD format.
        format (bool, optional): Set to False to return numeric data, or True to add % and £ where relevant

    Returns:
        df (dataframe): Pandas dataframe of results.

    """

    api_payload = {
        'start_date': start_date,
        'end_date': end_date,
        'metrics': 'ga:entrances, ga:sessions, ga:transactions, \
    ga:transactionsPerSession, ga:transactionRevenue, ga:revenuePerTransaction, \
    ga:adCost, ga:CPC',
        'dimensions': 'ga:yearMonth',
        'sort': '-ga:yearMonth',
        'filters': 'ga:medium==cpc;ga:source==google'
    }

    df_all = query.run_query(service, view, api_payload)

    df_all['date'] = pd.to_datetime(df_all['yearMonth'], format='%Y%m')
    df_all['yearMonth'] = df_all['date'].dt.strftime('%B, %Y')
    df_all = df_all.drop(columns=['date'])
    df_all = df_all.rename(columns={
        'yearMonth': 'Period',
        'entrances': 'Entrances',
        'sessions': 'Sessions',
        'transactions': 'Transactions',
        'transactionsPerSession': 'Conversion rate',
        'revenuePerTransaction': 'AOV',
        'transactionRevenue': 'Revenue',
        'adCost': 'Costs',
        'CPC': 'CPC',
    })

    df_all['COS'] = (df_all['Costs'] / df_all['Revenue']) * 100

    if format:
        df_all['Entrances'] = df_all['Entrances'].map('{:,.0f}'.format)
        df_all['Sessions'] = df_all['Sessions'].map('{:,.0f}'.format)
        df_all['Transactions'] = df_all['Transactions'].map('{:,.0f}'.format)
        df_all['Conversion rate'] = df_all['Conversion rate'].map('{:,.2f}%'.format)
        df_all['AOV'] = df_all['AOV'].map('£{:,.2f}'.format)
        df_all['Revenue'] = df_all['Revenue'].map('£{:,.0f}'.format)
        df_all['Costs'] = df_all['Costs'].map('£{:,.0f}'.format)
        df_all['CPC'] = df_all['CPC'].map('£{:,.2f}'.format)
        df_all['COS'] = df_all['COS'].map('{:,.2f}%'.format)

    return df_all
