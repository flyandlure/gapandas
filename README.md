# GAPandas
GAPandas is a Python package that lets you query the Google Analytics reporting API and return results in Pandas DataFrames, so they can be easily analysed, reported, or plotted in Python applications. It is a simple wrapper to Google's official API which is designed to reduce code and simplify development, especially from Jupyter Notebook environments.  

## Setup
GAPandas is easy to set up. First, you need to obtain a `client_secrets.json` keyfile from Google Analytics in order to authenticate. Google's [documentation](https://developers.google.com/analytics/devguides/config/mgmt/v3/quickstart/installed-py) explains how to do this. 

Once you have created a `client_secrets.json` file, download it and store it on your machine and note the path to the file. Add the associated email as a user in your Google Analytics account. 

## Basic example
To make a query, authenticate by running `connect.get_service()` passing it the path to your `client_secrets.json` keyfile. 

```python
from gapandas import connect, query

service = connect.get_service('path/to/client_secrets.json')
```

Now you have a connection, construct an API query to pass to the API. This "payload" must include a `start-date` and `end-date`, some `metrics` and some `dimensions` stored in a Python dictionary. 

The queries can sometimes be fiddly to write. I recommend using the [Google Analytics Query Explorer](https://ga-dev-tools.appspot.com/query-explorer/) to construct a valid API query or creating a prototype in Google Sheets. In the below example, we'll fetch sessions, pageviews and bounces by date for the past 30 days.


```python
payload = {
    'start_date': '30daysAgo',
    'end_date': 'today',
    'metrics': 'ga:sessions, ga:pageviews, ga:bounces',
    'dimensions': 'ga:date'
}
```

Now you can then use the `query.run_query()` function to pass your payload to the API, along with the service object and your Google Analytics view ID.

```python
results = query.run_query(service, '123456789', payload)
print(results)
```  
By default, this will return a Pandas DataFrame containing your query results. However, by passing the optional value of `'raw'` at the end of the function you can also return the raw data object. The `query` method also provides some other features to extract data from the `raw` object. 

```python
results = query.run_query(service, '123456789', payload, 'raw')
``` 

You can run multiple queries in succession and use the Pandas `merge()` function to connect these together. Pandas also makes it very easy to write the data to a file, such as a CSV or Excel document or write it to a database. You can use the data in reports, visualisations or machine learning models with very little code.

### Pagination
If you do not define `max_results` the API will return a default of 1000 rows in a single page. You can set this to a maximum of 10000 in your payload. 

Pagination is handled automatically. GAPandas will fetch each page of results and return them all in a single DataFrame (or object if you pass the `raw` flag in your query.)

### Changes

* Version 0.16 - Added `set_dtypes()` function to set the correct dtypes and improved error handling. 
* version 0.17 - Fixed bug in use of `exit()`
