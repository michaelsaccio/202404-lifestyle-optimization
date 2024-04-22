# Lifestyle Optimization using the FitBit API


## 1. Data Gathering
### `gather_awake_data.py`
This script gathers awake data using the Google Sheets API. It performs the following steps:
- Imports data using the Google Sheets API.
- Processes the data, splitting the 'Date' column and converting it to datetime format.
- Retrieves the most recent data from the 'database.csv' file.
- Selects new awake data based on the most recent date.
- Saves the updated data to 'database.csv'.

### `gather_asleep_data.py`
This script gathers asleep data using the Fitbit API. It involves the following functionalities:
- **OAuth2Server**: Handles the authorization process using CherryPy to set up a local server for OAuth2 authorization. It opens a browser to the authorization URL and waits for the user to grant access.
- **FitbitAPI**: Manages the Fitbit API client, including methods for fetching and handling access tokens.
- **fetch_and_format_sleep_data**: Fetches sleep data from the Fitbit API for a specified date range and formats it into a pandas DataFrame.
- **convert_sleep_data_to_dataframe**: Converts the raw sleep data obtained from the Fitbit API into a DataFrame format.

The script sets up a local server to handle the OAuth2 authorization flow, allowing the user to grant access to their Fitbit data. Once authorized, it fetches sleep data for a specified date range and formats it for further processing. Much of this code was borrowed from: https://github.com/orcasgit/python-fitbit/blob/master/gather_keys_oauth2.py

Ensure you have the necessary Fitbit API credentials and dependencies installed to use this script.


## 2. Data Processing and Storage
### `database_updater.py`
This script is responsible for updating the CSV database file (`database.csv`) with the most recent awake and asleep data. Here's a brief overview of its functionalities:

- **Importing Awake Data using the Google Sheets API**: Imports awake data from Google Sheets, splits the 'Date' column into 'DayOfWeek' and 'Date', converts the 'Date' column to datetime format, and selects new awake data based on the most recent date in the database.
- **Importing Asleep Data using the Fitbit API**: Imports asleep data from the Fitbit API, handles OAuth2 authorization using CherryPy, fetches sleep data for a specified date range, and formats it into a pandas DataFrame.
- **Merging and Appending New Data to the Database**: Merges the new awake and asleep dataframes on their 'Date' columns, appends the merged data to the existing database dataframe, removes any duplicate entries, and saves the updated dataframe to 'database.csv'.

### `sql_database_updater.py` (Using SQLite)
This script is identical to `database_updater.py` but uses SQLite for data storage. It initializes an SQLite connection and cursor, creates a table if it doesn't exist, and performs data insertion and retrieval operations similar to `database_updater.py`.

Using SQLite offers advantages such as ease of use, portability, and compatibility with various programming languages and platforms. It provides a lightweight, serverless database solution suitable for small to medium-sized applications.


## 3. Data Analysis and Machine Learning
### `analysis.py`
This script performs data analysis and machine learning tasks on the collected data. It includes the following sections:

### Data Importing and Cleaning
- Imports the data from 'database.csv' and performs cleaning tasks, such as dropping irrelevant columns and creating new columns.

### Feature Engineering
- Creates new features like 'totalScreenTime', 'totalProductivity', and 'minutesAfterMidnight'.
- Converts 'DayOfWeek' to integers for analysis.

### Exploratory Data Analysis (EDA)
- Visualizes 'Day Rating' by day of the week.
- Plots 'Day Rating' over time, both daily and weekly.
- Calculates correlations between features and visualizes them using a heatmap.
- Identifies statistically significant feature pairs based on correlation coefficients and p-values.

### Machine Learning Models
- Uses LASSO regression for feature selection.
- Runs Ordinary Least Squares (OLS) regression for analysis.
- Builds and trains a Deep Neural Network (DNN) for prediction.

### Final Outputs
- Prints coefficients from LASSO regression.
- Displays summary of OLS regression.
- Prints feature weights from the trained DNN.

## Prerequisites
- Ensure you have the necessary credentials for accessing the Google Sheets API and Fitbit API.
- Install the required Python packages listed in each script.

## Usage
- Run `database_updater.py` or `sql_database_updater.py` to collect and store current data.
- Run `analysis.py` for data analysis and machine learning tasks.

## Dependencies
- Python 3.x
- Libraries: pandas, numpy, seaborn, matplotlib, scipy, scikit-learn, statsmodels, torch

Feel free to reach out if you have any questions or suggestions!
