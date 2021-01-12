"""
Name: Runs a Google Analytics API query
Developer: Matt Clarke
Date: June 8, 2020
Description: Passes a payload to the Google Analytics reporting API and returns the data.
"""

import math
import pandas as pd


def show_message(verbose, message):
    """Show a message if verbose mode is True.

    Args:
        verbose (bool): True to display messages
        message (str): Message to display.

    Returns:
        Print message if verbose mode is True.
    """

    if verbose:
        print(message)


def run_query(service: object,
              view_id: str,
              payload: dict,
              output: str = 'df',
              verbose=False):
    """Runs a query against the Google Analytics reporting API and returns the results data.

    Args:
        service (object): Authenticated Google Analytics service connection
        view_id (int): Google Analytics view ID to query
        payload (dict): Payload of query parameters to pass to Google Analytics in Python dictionary
        output (str): String containing the format to return (df or raw)
        verbose (bool): Turn on verbose messages.

    Returns:
         Pandas dataframe or raw array
    """

    required_payload = {'ids': 'ga:' + view_id}
    final_payload = {**required_payload, **payload}

    try:
        results = get_results(service, final_payload)
        show_message(verbose, results)

        if output == 'df':
            return results_to_pandas(results)
        else:
            return results

    except Exception as e:
        print('Query failed:', str(e))


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


def set_dtypes(df):
    """Sets the correct data type for each column returned in the dataframe.

    :param df: Pandas dataframe from Google Analytics API query
    :return: Pandas dataframe with correct dtypes assigned to columns
    """

    integer_dtype = ['sessionCount', 'daysSinceLastSession', 'userBucket', 'users', 'newUsers', '1dayUsers',
                     '7dayUsers', '14dayUsers', '28dayUsers', '30dayUsers', 'sessionDurationBucket', 'sessions',
                     'bounces', 'uniqueDimensionCombinations', 'hits', 'organicSearches', 'impressions', 'adclicks',
                     'goal1Starts', 'goal2Starts', 'goal3Starts', 'goal4Starts', 'goal5Starts', 'goal6Starts',
                     'goal7Starts', 'goal8Starts', 'goal9Starts', 'goal10Starts', 'goal11Starts', 'goal12Starts',
                     'goal13Starts', 'goal14Starts', 'goal15Starts', 'goal16Starts', 'goal17Starts', 'goal18Starts',
                     'goal19Starts', 'goal20Starts', 'goal1Completions', 'goal2Completions', 'goal3Completions',
                     'goal4Completions', 'goal5Completions', 'goal6Completions', 'goal7Completions', 'goal8Completions',
                     'goal9Completions', 'goal10Completions', 'goal11Completions', 'goal12Completions',
                     'goal13Completions', 'goal14Completions', 'goal15Completions', 'goal16Completions',
                     'goal17Completions', 'goal18Completions', 'goal19Completions', 'goal20Completions',
                     'goalCompletionsAll', 'goalStartsAll', 'goal1Abandons', 'goal2Abandons', 'goal3Abandons',
                     'goal4Abandons', 'goal5Abandons', 'goal6Abandons', 'goal7Abandons', 'goal8Abandons',
                     'goal9Abandons', 'goal10Abandons', 'goal11Abandons', 'goal12Abandons', 'goal13Abandons',
                     'goal14Abandons', 'goal15Abandons', 'goal16Abandons', 'goal17Abandons', 'goal18Abandons',
                     'goal19Abandons', 'goal20Abandons', 'goalAbandonsAll', 'pageDepth', 'entrances', 'pageviews',
                     'uniquePageviews', 'exits', 'searchResultViews', 'searchUniques', 'searchSessions', 'searchDepth',
                     'searchRefinements', 'searchExits', 'pageLoadTime', 'pageLoadSample', 'domainLookupTime',
                     'pageDownloadTime', 'redirectionTime', 'serverConnectionTime', 'serverResponseTime',
                     'speedMetricsSample', 'domInteractiveTime', 'domContentLoadedTime', 'domLatencyMetricsSample',
                     'screenviews', 'uniqueScreenviews', 'sessionsWithEvent', 'sessionsToTransaction',
                     'daysToTransaction', 'transactions', 'itemQuantity', 'uniquePurchases', 'internalPromotionClicks',
                     'internalPromotionViews', 'productAddsToCart', 'productCheckouts', 'productDetailViews',
                     'productListClicks', 'productListViews', 'productRefunds', 'productRemovesFromCart',
                     'quantityAddedToCart', 'quantityCheckedOut', 'quantityRefunded', 'quantityRemovedFromCart',
                     'totalRefunds', 'socialInteractions', 'uniqueSocialInteractions', 'userTimingValue',
                     'userTimingSample', 'exceptions', 'fatalExceptions', 'dimension1', 'dimension2', 'dimension3',
                     'dimension4', 'dimension5', 'dimension6', 'dimension7', 'dimension8', 'dimension9', 'dimension10',
                     'dimension11', 'dimension12', 'dimension13', 'dimension14', 'dimension15', 'dimension16',
                     'dimension17', 'dimension18', 'dimension19', 'dimension20', 'customMetric1', 'customMetric2',
                     'customMetric3', 'customMetric4', 'customMetric5', 'customMetric6', 'customMetric7',
                     'customMetric8', 'customMetric9', 'customMetric10', 'customMetric11', 'customMetric12',
                     'customMetric13', 'customMetric14', 'customMetric15', 'customMetric16', 'customMetric17',
                     'customMetric18', 'customMetric19', 'customMetric20', 'year', 'month', 'week', 'day', 'hour',
                     'minute', 'nthMonth', 'nthWeek', 'nthDay', 'nthMinute', 'dayOfWeek', 'isoWeek', 'isoYear',
                     'isoYearIsoWeek', 'nthHour', 'dcmFloodlightQuantity', 'dcmClicks', 'dcmImpressions',
                     'adsenseAdUnitsViewed', 'adsenseAdsViewed', 'adsenseAdsClicks', 'adsensePageImpressions',
                     'adsenseExits', 'totalPublisherImpressions', 'totalPublisherMonetizedPageviews',
                     'totalPublisherClicks', 'backfillImpressions', 'backfillMonetizedPageviews', 'backfillClicks',
                     'dfpImpressions', 'dfpMonetizedPageviews', 'dfpClicks', 'cohortNthDay', 'cohortNthMonth',
                     'cohortNthWeek', 'cohortActiveUsers', 'cohortTotalUsers', 'cohortTotalUsersWithLifetimeCriteria',
                     'dbmClicks', 'dbmConversions', 'dbmImpressions', 'dsCost', 'dsImpressions'
                     ]

    float_dtype = ['percentNewSessions', 'sessionsPerUser', 'bounceRate', 'adCost', 'CPM', 'CPC', 'CTR',
                   'costPerTransaction', 'costPerGoalConversion', 'RPC', 'ROAS', 'goal1Value', 'goal2Value',
                   'goal3Value', 'goal4Value', 'goal5Value', 'goal6Value', 'goal7Value', 'goal8Value', 'goal9Value',
                   'goal10Value', 'goal11Value', 'goal12Value', 'goal13Value', 'goal14Value', 'goal15Value',
                   'goal16Value', 'goal17Value', 'goal18Value', 'goal19Value', 'goal20Value', 'goalValueAll',
                   'goalValuePerSession', 'goal1ConversionRate', 'goal2ConversionRate', 'goal3ConversionRate',
                   'goal4ConversionRate', 'goal5ConversionRate', 'goal6ConversionRate', 'goal7ConversionRate',
                   'goal8ConversionRate', 'goal9ConversionRate', 'goal10ConversionRate', 'goal11ConversionRate',
                   'goal12ConversionRate', 'goal13ConversionRate', 'goal14ConversionRate', 'goal15ConversionRate',
                   'goal16ConversionRate', 'goal17ConversionRate', 'goal18ConversionRate', 'goal19ConversionRate',
                   'goal20ConversionRate', 'goalConversionRateAll', 'goal1AbandonRate', 'goal2AbandonRate',
                   'goal3AbandonRate', 'goal4AbandonRate', 'goal5AbandonRate', 'goal6AbandonRate', 'goal7AbandonRate',
                   'goal8AbandonRate', 'goal9AbandonRate', 'goal10AbandonRate', 'goal11AbandonRate',
                   'goal12AbandonRate', 'goal13AbandonRate', 'goal14AbandonRate', 'goal15AbandonRate',
                   'goal16AbandonRate', 'goal17AbandonRate', 'goal18AbandonRate', 'goal19AbandonRate',
                   'goal20AbandonRate', 'goalAbandonRateAll', 'latitude', 'longitude', 'pageValue', 'entranceRate',
                   'pageviewsPerSession', 'exitRate', 'avgSearchResultViews', 'percentSessionsWithSearch',
                   'avgSearchDepth', 'percentSearchRefinements', 'searchExitRate', 'searchGoalConversionRateAll',
                   'goalValueAllPerSearch', 'searchGoal1ConversionRate', 'searchGoal2ConversionRate',
                   'searchGoal3ConversionRate', 'searchGoal4ConversionRate', 'searchGoal5ConversionRate',
                   'searchGoal6ConversionRate', 'searchGoal7ConversionRate', 'searchGoal8ConversionRate',
                   'searchGoal9ConversionRate', 'searchGoal10ConversionRate', 'searchGoal11ConversionRate',
                   'searchGoal12ConversionRate', 'searchGoal13ConversionRate', 'searchGoal14ConversionRate',
                   'searchGoal15ConversionRate', 'searchGoal16ConversionRate', 'searchGoal17ConversionRate',
                   'searchGoal18ConversionRate', 'searchGoal19ConversionRate', 'searchGoal20ConversionRate',
                   'avgPageLoadTime', 'avgDomainLookupTime', 'avgPageDownloadTime', 'avgRedirectionTime',
                   'avgServerConnectionTime', 'avgServerResponseTime', 'avgDomInteractiveTime',
                   'avgDomContentLoadedTime', 'avgDomLatencyMetricsSample', 'screenviewsPerSession',
                   'avgScreenviewDuration', 'eventValue', 'eventsPerSessionWithEvent', 'transactionsPerSession',
                   'transactionRevenue', 'revenuePerTransaction', 'transactionRevenuePerSession', 'transactionShipping',
                   'transactionTax', 'totalValue', 'revenuePerItem', 'itemRevenue', 'itemsPerPurchase',
                   'localTransactionRevenue', 'localTransactionShipping', 'localTransactionTax', 'localItemRevenue',
                   'buyToDetailRate', 'cartToDetailRate', 'internalPromotionCTR', 'localProductRefundAmount',
                   'localRefundAmount', 'productListCTR', 'productRefundAmount', 'productRevenuePerPurchase',
                   'refundAmount', 'revenuePerUser', 'transactionsPerUser', 'socialInteractionsPerSession',
                   'avgUserTimingValue', 'exceptionsPerScreenview', 'fatalExceptionsPerScreenview',
                   'dcmFloodlightRevenue', 'dcmCPC', 'dcmCTR', 'dcmCost', 'dcmROAS', 'dcmRPC', 'adsenseRevenue',
                   'adsenseCTR', 'adsenseECPM', 'adsenseViewableImpressionPercent', 'adsenseCoverage',
                   'totalPublisherCoverage', 'totalPublisherImpressionsPerSession', 'totalPublisherECPM',
                   'totalPublisherViewableImpressionsPercent', 'totalPublisherCTR', 'totalPublisherRevenue',
                   'totalPublisherRevenuePer1000Sessions', 'adxImpressions', 'adxMonetizedPageviews', 'adxClicks',
                   'adxCoverage', 'adxImpressionsPerSession', 'adxViewableImpressionsPercent', 'adxCTR', 'adxRevenue',
                   'adxRevenuePer1000Sessions', 'adxECPM', 'backfillCoverage', 'backfillImpressionsPerSession',
                   'backfillViewableImpressionsPercent', 'backfillCTR', 'backfillRevenue', 'backfillECPM',
                   'backfillRevenuePer1000Sessions', 'dfpCoverage', 'dfpImpressionsPerSession',
                   'dfpViewableImpressionsPercent', 'dfpCTR', 'dfpRevenue', 'dfpRevenuePer1000Sessions', 'dfpECPM',
                   'cohortAppviewsPerUser', 'cohortAppviewsPerUserWithLifetimeCriteria', 'cohortGoalCompletionsPerUser',
                   'cohortGoalCompletionsPerUserWithLifetimeCriteria', 'cohortPageviewsPerUser',
                   'cohortPageviewsPerUserWithLifetimeCriteria', 'cohortRetentionRate', 'cohortRevenuePerUser',
                   'cohortRevenuePerUserWithLifetimeCriteria', 'cohortSessionDurationPerUser',
                   'cohortSessionDurationPerUserWithLifetimeCriteria', 'cohortSessionsPerUser',
                   'cohortSessionsPerUserWithLifetimeCriteria', 'dbmCPA', 'dbmCPC', 'dbmCPM', 'dbmCTR', 'dbmCost',
                   'dbmROAS', 'dsCPC', 'dsCTR', 'dsProfit', 'dsReturnOnAdSpend', 'dsRevenuePerClick'
                   ]

    string_dtype = ['userType', 'userDefinedValue', 'referralPath', 'fullReferrer', 'campaign', 'source', 'medium',
                    'sourceMedium', 'keyword', 'adContent', 'socialNetwork', 'hasSocialSourceReferral',
                    'campaignCode', 'adGroup', 'adSlot', 'adDistributionNetwork', 'adMatchType',
                    'adKeywordMatchType', 'adMatchedQuery', 'adPlacementDomain', 'adPlacementUrl', 'adFormat',
                    'adTargetingType', 'adTargetingOption', 'adDisplayUrl', 'adDestinationUrl',
                    'adwordsCustomerID', 'adwordsCampaignID', 'adwordsAdGroupID', 'adwordsCreativeID',
                    'adwordsCriteriaID', 'adQueryWordCount', 'isTrueViewVideoAd', 'goalCompletionLocation',
                    'goalPreviousStep1', 'goalPreviousStep2', 'goalPreviousStep3', 'browser', 'browserVersion',
                    'operatingSystem', 'operatingSystemVersion', 'mobileDeviceBranding', 'mobileDeviceModel',
                    'mobileDeviceInputSelector', 'mobileDeviceInfo', 'mobileDeviceMarketingName', 'deviceCategory',
                    'browserSize', 'dataSource', 'continent', 'subContinent', 'country', 'region', 'metro', 'city',
                    'networkDomain', 'cityId', 'continentId', 'countryIsoCode', 'metroId', 'regionId', 'regionIsoCode',
                    'subContinentCode', 'flashVersion', 'javaEnabled', 'language', 'screenColors',
                    'sourcePropertyDisplayName', 'sourcePropertyTrackingId', 'screenResolution', 'hostname', 'pagePath',
                    'pagePathLevel1', 'pagePathLevel2', 'pagePathLevel3', 'pagePathLevel4', 'pageTitle',
                    'landingPagePath', 'secondPagePath', 'exitPagePath', 'previousPagePath', 'searchUsed',
                    'searchKeyword', 'searchKeywordRefinement', 'searchCategory', 'searchStartPage',
                    'searchDestinationPage', 'searchAfterDestinationPage', 'appInstallerId', 'appVersion', 'appName',
                    'appId', 'screenName', 'screenDepth', 'landingScreenName', 'exitScreenName', 'eventCategory',
                    'eventAction', 'eventLabel', 'transactionId', 'affiliation', 'productSku', 'productName',
                    'productCategory', 'currencyCode', 'checkoutOptions', 'internalPromotionCreative',
                    'internalPromotionId', 'internalPromotionName', 'internalPromotionPosition', 'orderCouponCode',
                    'productBrand', 'productCategoryHeirarchy', 'productCouponCode', 'productListName',
                    'productListPosition', 'productVariant', 'shoppingStage', 'socialInteractionNetwork',
                    'socialInteractionAction', 'socialInteractionNetworkAction', 'socialInteractionTarget',
                    'socialEngagementType', 'userTimingCategory', 'userTimingLabel', 'userTimingVariable',
                    'exceptionDescription', 'experimentId', 'experimentVariant', 'experimentCombination',
                    'experimentName', 'customVarName1', 'customVarName2', 'customVarName3', 'customVarName4',
                    'customVarName5', 'customVarName6', 'customVarName7', 'customVarName8', 'customVarName9',
                    'customVarName10', 'customVarName11', 'customVarName12', 'customVarName13', 'customVarName14',
                    'customVarName15', 'customVarName16', 'customVarName17', 'customVarName18', 'customVarName19',
                    'customVarName20', 'customVarValue1', 'customVarValue2', 'customVarValue3', 'customVarValue4',
                    'customVarValue5', 'customVarValue6', 'customVarValue7', 'customVarValue8', 'customVarValue9',
                    'customVarValue10', 'customVarValue11', 'customVarValue12', 'customVarValue13', 'customVarValue14',
                    'customVarValue15', 'customVarValue16', 'customVarValue17', 'customVarValue18', 'customVarValue19',
                    'customVarValue20', 'dayOfWeekName', 'dateHour', 'dateHourMinute', 'yearMonth', 'yearWeek',
                    'dcmClickAd', 'dcmClickAdId', 'dcmClickAdType', 'dcmClickAdTypeId', 'ga:dcmClickAdvertiser',
                    'dcmClickAdvertiserId', 'dcmClickCampaign', 'dcmClickCampaignId', 'dcmClickCreative',
                    'dcmClickCreativeId', 'dcmClickRenderingId', 'dcmClickCreativeType', 'dcmClickCreativeTypeId',
                    'dcmClickCreativeVersion', 'dcmClickSite', 'dcmClickSiteId', 'dcmClickSitePlacement',
                    'dcmClickSitePlacementId', 'dcmClickSpotId', 'dcmFloodlightActivity',
                    'dcmFloodlightActivityAndGroup', 'dcmFloodlightActivityGroup', 'dcmFloodlightActivityGroupId',
                    'dcmFloodlightActivityId', 'dcmFloodlightAdvertiserId', 'dcmFloodlightSpotId', 'dcmLastEventAd',
                    'dcmLastEventAdId', 'dcmLastEventAdType', 'dcmLastEventAdTypeId', 'dcmLastEventAdvertiser',
                    'dcmLastEventAdvertiserId', 'dcmLastEventAttributionType', 'dcmLastEventCampaign',
                    'dcmLastEventCampaignId', 'dcmLastEventCreative', 'dcmLastEventCreativeId',
                    'dcmLastEventRenderingId', 'dcmLastEventCreativeType', 'dcmLastEventCreativeTypeId',
                    'dcmLastEventCreativeVersion', 'dcmLastEventSite', 'dcmLastEventSiteId',
                    'dcmLastEventSitePlacement', 'dcmLastEventSitePlacementId', 'dcmLastEventSpotId', 'userAgeBracket',
                    'userGender', 'interestOtherCategory', 'interestAffinityCategory', 'interestInMarketCategory',
                    'dfpLineItemId', 'dfpLineItemName', 'acquisitionCampaign', 'acquisitionMedium', 'acquisitionSource',
                    'acquisitionSourceMedium', 'acquisitionTrafficChannel', 'cohort', 'channelGrouping',
                    'dbmClickAdvertiser', 'dbmClickAdvertiserId', 'dbmClickCreativeId', 'dbmClickExchange',
                    'dbmClickExchangeId', 'dbmClickInsertionOrder', 'dbmClickInsertionOrderId', 'dbmClickLineItem',
                    'dbmClickLineItemId', 'dbmClickSite', 'dbmClickSiteId', 'dbmLastEventAdvertiser',
                    'dbmLastEventAdvertiserId', 'dbmLastEventCreativeId', 'dbmLastEventExchange',
                    'dbmLastEventExchangeId', 'dbmLastEventInsertionOrder', 'dbmLastEventInsertionOrderId',
                    'dbmLastEventLineItem', 'dbmLastEventLineItemId', 'dbmLastEventSite', 'dbmLastEventSiteId',
                    'dsAdGroup', 'dsAdGroupId', 'dsAdvertiser', 'dsAdvertiserId', 'dsAgency', 'dsAgencyId',
                    'dsCampaign', 'dsCampaignId', 'dsEngineAccount', 'dsEngineAccountId', 'dsKeyword', 'dsKeywordId'
                    ]

    date_dtype = ['date']
    time_dtype = ['time', 'avgSessionDuration', 'timeOnPage', 'avgTimeOnPage', 'searchDuration', 'timeOnScreen']

    for column in df.columns:
        if column in integer_dtype:
            df[column] = df[column].astype(int)
        elif column in float_dtype:
            df[column] = df[column].astype(float)
        elif column in date_dtype:
            df[column] = pd.to_datetime(df[column])
        elif column in string_dtype:
            df[column] = df[column].astype(str)
        elif column in time_dtype:
            df[column] = df[column].astype(str)
        else:
            df[column] = df[column]
    return df


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

            df = pd.DataFrame(rows, columns=headings)
            return set_dtypes(df)


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
