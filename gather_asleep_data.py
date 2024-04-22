import cherrypy
import webbrowser
import threading
import traceback
import pandas as pd
from urllib.parse import urlparse
from datetime import datetime, date
import fitbit
import requests
from fitbit.api import Fitbit
from oauthlib.oauth2.rfc6749.errors import MismatchingStateError, MissingTokenError
from fitbit.exceptions import HTTPUnauthorized

# Fitbit credentials
client_id = ""
client_secret = ""
redirect_uri = '/'

# FitbitAPI class to handle Fitbit API client
class FitbitAPI:
    def __init__(self, client_id, client_secret, access_token=None, refresh_token=None, redirect_uri=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.redirect_uri = redirect_uri

    def get_authorized_client(self):
        return Fitbit(self.client_id, self.client_secret,
                      access_token=self.access_token, refresh_token=self.refresh_token,
                      redirect_uri=self.redirect_uri)

# OAuth2Server class for handling authorization
class OAuth2Server:
    def __init__(self, client_id, client_secret, redirect_uri='http://127.0.0.1:8080/'):
        self.success_html = """
        <h1>You are now authorized to access the Fitbit API!</h1>
        <br/><h3>You can close this window</h3>"""
        self.failure_html = """
        <h1>ERROR: %s</h1><br/><h3>You can close this window</h3>%s"""
        self.fitbit = Fitbit(
            client_id,
            client_secret,
            redirect_uri=redirect_uri,
            timeout=10,
        )
        self.redirect_uri = redirect_uri

    def browser_authorize(self):
        """
        Open a browser to the authorization url and spool up a CherryPy
        server to accept the response
        """
        url, _ = self.fitbit.client.authorize_token_url()
        # Open the web browser in a new thread for command-line browser support
        threading.Timer(1, webbrowser.open, args=(url,)).start()
        # Same with redirect_uri hostname and port.
        urlparams = urlparse(self.redirect_uri)
        cherrypy.config.update({'server.socket_host': urlparams.hostname,
                                'server.socket_port': urlparams.port})
        cherrypy.quickstart(self)

    @cherrypy.expose
    def index(self, state, code=None, error=None):
        """
        Receive a Fitbit response containing a verification code. Use the code
        to fetch the access_token.
        """
        error = None
        if code:
            try:
                self.fitbit.client.fetch_access_token(code)
            except MissingTokenError:
                error = self._fmt_failure(
                    'Missing access token parameter.</br>Please check that '
                    'you are using the correct client_secret')
            except MismatchingStateError:
                error = self._fmt_failure('CSRF Warning! Mismatching state')
        else:
            error = self._fmt_failure('Unknown error while authenticating')

        # Use a thread to shutdown cherrypy so we can return HTML first
        self._shutdown_cherrypy()
        return error if error else self.success_html

    def _fmt_failure(self, message):
        tb = traceback.format_tb(sys.exc_info()[2])
        tb_html = '<pre>%s</pre>' % ('\n'.join(tb)) if tb else ''
        return self.failure_html % (message, tb_html)

    def _shutdown_cherrypy(self):
        """ Shutdown cherrypy in one second, if it's running """
        if cherrypy.engine.state == cherrypy.engine.states.STARTED:
            threading.Timer(1, cherrypy.engine.exit).start()

def fetch_and_format_sleep_data(start_date, end_date, fitbit_client):
    all_sleep_data_df = pd.DataFrame()  # Initialize DataFrame
    date_range = pd.date_range(start_date, end_date)  # Generate date range
    for date in date_range:
        formatted_date = date.strftime('%Y-%m-%d')
        try:
            sleep_data = fitbit_client.get_sleep(date=date)  # Fetch sleep data using authorized client
            daily_sleep_df = convert_sleep_data_to_dataframe(sleep_data)  # Convert to DataFrame
            daily_sleep_df['date'] = formatted_date  # Add date column
            all_sleep_data_df = pd.concat([all_sleep_data_df, daily_sleep_df], ignore_index=True)  # Append to main DataFrame
        except HTTPUnauthorized:
            print(f"Failed to fetch sleep data for {formatted_date}: Unauthorized access")  # Print error
    return all_sleep_data_df

def convert_sleep_data_to_dataframe(sleep_data):
    sleep_records = sleep_data['sleep']
    formatted_sleep_records = []
    for record in sleep_records:
        record['date'] = record['dateOfSleep']  # Rename 'dateOfSleep' to 'date'
        del record['dateOfSleep']  # Delete 'dateOfSleep' key
        formatted_sleep_records.append(record)
    return pd.DataFrame(formatted_sleep_records)  # Return DataFrame
