import pandas as pd
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Scopes, Google Sheet ID, and range
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SHEET_ID = ''
RANGE = ''

def get_sheet_data():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('api_files/awake/token.json'):
        creds = Credentials.from_authorized_user_file('api_files/awake/token.json', SCOPES) # Adjusted path for token.json as well
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'api_files/awake/credentials.json', SCOPES)  # Adjusted path as needed
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('api_files/awake/token.json', 'w') as token: # Adjust the path for token.json
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SHEET_ID, range=RANGE).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
        return pd.DataFrame()  # Return an empty DataFrame if no data found
    else:
        df = pd.DataFrame(values[1:], columns=values[0])  # Use the first row as column names
        df.dropna(inplace=True)  # Drop rows with None values
        return df

def main():
    df = get_sheet_data()
    return df

if __name__ == '__main__':
    dataframe = main()
    awake_df = main()
